from pydantic import BaseModel
from typing import Any, Dict

class GovernanceContext(BaseModel):
    journey: str
    actor: Dict[str, Any]
    input: Dict[str, Any]
    requestContext: Dict[str, Any] | None = None
    metadata: Dict[str, Any] | None = None
