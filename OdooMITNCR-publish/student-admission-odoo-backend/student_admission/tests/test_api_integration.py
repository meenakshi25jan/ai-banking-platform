# -*- coding: utf-8 -*-
"""Integration tests for REST API endpoints."""

from odoo.tests import tagged, HttpCase


@tagged('post_install', '-at_install')
class TestAdmissionAPI(HttpCase):

  def test_public_courses_endpoint(self):
    self.authenticate(None, None)
    response = self.url_open('/api/v1/courses')
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertEqual(data['status'], 'success')
    self.assertIsInstance(data['data'], list)

  def test_public_registration_endpoint(self):
    self.authenticate(None, None)
    payload = {
      'first_name': 'API',
      'last_name': 'Test',
      'email': 'api.test.unique@example.com',
      'mobile': '9111111199',
      'date_of_birth': '2005-05-05',
      'gender': 'male',
      'address': 'API Test Address',
      'parent_name': 'Parent API',
      'parent_mobile': '9222222299',
      'aadhaar_number': '555566667777',
    }
    response = self.url_open(
      '/api/v1/registrations',
      data=payload,
      headers={'Content-Type': 'application/json'},
    )
    self.assertIn(response.status_code, (200, 201))
    data = response.json()
    self.assertEqual(data['status'], 'success')
    self.assertTrue(data['data']['registration_number'])

  def test_dashboard_requires_auth(self):
    response = self.url_open('/api/v1/dashboard')
    self.assertIn(response.status_code, (401, 403, 303))
