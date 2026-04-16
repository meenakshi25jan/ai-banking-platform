"""
Amazon Bedrock LLM Client — Primary AI provider for the banking platform.
Primary provider: Amazon Bedrock Claude 3 Sonnet.
Fallback provider: self-managed OpenAI-compatible LLM endpoint (Meta-Llama/Qwen).
Tertiary fallback: OpenAI if API key is configured.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from collections import OrderedDict
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_bedrock_client = None
_openai_client = None
_CACHE: OrderedDict[str, tuple[float, str]] = OrderedDict()
_CACHE_MAX = int(os.getenv("LLM_CACHE_MAX", "128"))
_CACHE_TTL = int(os.getenv("LLM_CACHE_TTL_SECONDS", "300"))
_TIMEOUT = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))


def _cache_key(*parts: object) -> str:
    raw = "||".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _get_cached(key: str) -> Optional[str]:
    now = time.time()
    item = _CACHE.get(key)
    if not item:
        return None
    expires_at, value = item
    if expires_at < now:
        _CACHE.pop(key, None)
        return None
    _CACHE.move_to_end(key)
    return value


def _set_cached(key: str, value: str) -> None:
    _CACHE[key] = (time.time() + _CACHE_TTL, value)
    _CACHE.move_to_end(key)
    while len(_CACHE) > _CACHE_MAX:
        _CACHE.popitem(last=False)


def _get_bedrock_client():
    global _bedrock_client
    if _bedrock_client is None:
        try:
            import boto3
            client_kwargs = {"region_name": os.getenv("AWS_REGION", "us-west-2")}
            if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
                client_kwargs.update({
                    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                })
            _bedrock_client = boto3.client("bedrock-runtime", **client_kwargs)
            logger.info("Amazon Bedrock runtime client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Bedrock client: {e}")
            _bedrock_client = None
    return _bedrock_client


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                _openai_client = OpenAI(api_key=api_key)
                logger.info("OpenAI tertiary fallback client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI client: {e}")
    return _openai_client


def invoke_llm(
    prompt: str,
    system_prompt: str = "You are Sentinel AI, a safe and trustworthy banking governance assistant.",
    max_tokens: int = 1024,
    temperature: float = 0.3,
    model_id: Optional[str] = None,
) -> str:
    cache_key = _cache_key(prompt, system_prompt, max_tokens, temperature, model_id or "")
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    for provider in (
        lambda: _invoke_bedrock(prompt, system_prompt, max_tokens, temperature, model_id),
        lambda: _invoke_fallback_endpoint(prompt, system_prompt, max_tokens, temperature),
        lambda: _invoke_openai(prompt, system_prompt, max_tokens, temperature),
    ):
        response = provider()
        if response:
            _set_cached(cache_key, response)
            return response

    return "I'm experiencing technical difficulties. Please try again shortly."


def _invoke_bedrock(prompt: str, system_prompt: str, max_tokens: int, temperature: float, model_id: Optional[str] = None) -> Optional[str]:
    client = _get_bedrock_client()
    if not client:
        return None
    model = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": prompt}],
        })
        response = client.invoke_model(
            modelId=model,
            contentType="application/json",
            accept="application/json",
            body=body,
        )
        result = json.loads(response["body"].read())
        text = result.get("content", [{}])[0].get("text", "")
        if text:
            logger.info("Bedrock response received")
            return text
    except Exception as e:
        logger.warning(f"Bedrock invocation failed: {e}")
    return None


def _invoke_fallback_endpoint(prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
    base_url = os.getenv("FALLBACK_BASE_URL", "").strip().rstrip("/")
    if not base_url:
        return None
    model = os.getenv("FALLBACK_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")
    headers = {"Content-Type": "application/json"}
    if os.getenv("FALLBACK_API_KEY"):
        headers["Authorization"] = f"Bearer {os.getenv('FALLBACK_API_KEY')}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        response = requests.post(f"{base_url}/v1/chat/completions", json=payload, headers=headers, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content")
        if text:
            logger.info("Fallback endpoint response received")
            return text
    except Exception as e:
        logger.warning(f"Fallback endpoint invocation failed: {e}")
    return None


def _invoke_openai(prompt: str, system_prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
    client = _get_openai_client()
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = response.choices[0].message.content
        if text:
            logger.info("OpenAI tertiary fallback response received")
            return text
    except Exception as e:
        logger.warning(f"OpenAI invocation failed: {e}")
    return None


def get_provider_status() -> dict:
    fallback = bool(os.getenv("FALLBACK_BASE_URL"))
    bedrock_ok = _get_bedrock_client() is not None
    openai_ok = _get_openai_client() is not None
    return {
        "bedrock": {"available": bedrock_ok, "model": os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")},
        "fallback_endpoint": {"available": fallback, "model": os.getenv("FALLBACK_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")},
        "openai": {"available": openai_ok, "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini")},
        "primary": "bedrock" if bedrock_ok else ("fallback_endpoint" if fallback else ("openai" if openai_ok else "none")),
        "cache": {"size": len(_CACHE), "ttl_seconds": _CACHE_TTL},
    }
