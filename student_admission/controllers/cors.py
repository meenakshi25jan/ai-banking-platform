# -*- coding: utf-8 -*-
import json
import os

from odoo import http
from odoo.http import request


class CorsMixin:
  """Add CORS headers for Next.js / Vercel frontend."""

  def _cors_headers(self):
    allowed = os.environ.get(
      'STUDENT_ADMISSION_CORS_ORIGINS',
      'http://localhost:3000,https://*.vercel.app',
    )
    origin = request.httprequest.headers.get('Origin', '')
    headers = {
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      'Access-Control-Allow-Credentials': 'true',
    }
    if origin:
      origins = [o.strip() for o in allowed.split(',')]
      if origin in origins or any(
        o.startswith('https://*.') and origin.endswith(o.split('*.')[1])
        for o in origins if o.startswith('https://*.')
      ) or 'localhost' in origin:
        headers['Access-Control-Allow-Origin'] = origin
    return headers

  def _json_response(self, data, status=200):
    headers = {'Content-Type': 'application/json'}
    headers.update(self._cors_headers())
    return request.make_response(json.dumps(data), status=status, headers=headers)

  def _handle_options(self):
    if request.httprequest.method == 'OPTIONS':
      return request.make_response('', headers=self._cors_headers())
