# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request


class StudentAdmissionAPI(http.Controller):

  @http.route('/api/student/admissions', type='http', auth='user', methods=['GET'], csrf=False)
  def list_admissions(self, **kwargs):
    admissions = request.env['student.admission.application'].search([])
    data = [{
      'id': rec.id,
      'admission_number': rec.name,
      'student_name': rec.full_name,
      'state': rec.state,
      'course': rec.course_id.name,
      'department': rec.department_id.name,
    } for rec in admissions]
    return request.make_response(
      json.dumps({'status': 'success', 'data': data}),
      headers=[('Content-Type', 'application/json')],
    )

  @http.route('/api/student/admissions/<int:admission_id>', type='http', auth='user', methods=['GET'], csrf=False)
  def get_admission(self, admission_id, **kwargs):
    admission = request.env['student.admission.application'].browse(admission_id)
    if not admission.exists():
      return request.make_response(
        json.dumps({'status': 'error', 'message': 'Admission not found'}),
        status=404,
        headers=[('Content-Type', 'application/json')],
      )
    data = {
      'id': admission.id,
      'admission_number': admission.name,
      'student_name': admission.full_name,
      'state': admission.state,
      'course': admission.course_id.name,
      'department': admission.department_id.name,
      'total_fee': admission.total_fee,
      'paid_fee': admission.paid_fee,
      'pending_fee': admission.pending_fee,
    }
    return request.make_response(
      json.dumps({'status': 'success', 'data': data}),
      headers=[('Content-Type', 'application/json')],
    )

  @http.route('/api/student/registrations', type='json', auth='user', methods=['POST'])
  def create_registration(self, **kwargs):
    payload = request.dispatcher.jsonrequest or {}
    required = ['first_name', 'last_name', 'email', 'mobile', 'date_of_birth', 'gender', 'address', 'parent_name', 'parent_mobile']
    missing = [field for field in required if not payload.get(field)]
    if missing:
      return {'status': 'error', 'message': 'Missing fields: %s' % ', '.join(missing)}
    registration = request.env['student.registration'].create(payload)
    return {
      'status': 'success',
      'registration_number': registration.name,
      'id': registration.id,
    }
