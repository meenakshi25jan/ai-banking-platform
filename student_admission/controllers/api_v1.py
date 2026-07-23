# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

from .cors import CorsMixin

_logger = logging.getLogger(__name__)


class StudentAdmissionAPIv1(http.Controller, CorsMixin):

  # ── Health ────────────────────────────────────────────────────────

  @http.route('/api/health', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
  @http.route('/api/v1/health', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
  def health(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    database = request.db or 'none'
    db_ok = False
    if request.db:
      try:
        request.env.cr.execute('SELECT 1')
        db_ok = True
      except Exception:
        db_ok = False
    payload = {
      'status': 'ok' if db_ok or not request.db else 'degraded',
      'service': 'student-admission-odoo',
      'database': database,
      'db_connected': db_ok,
    }
    status_code = 200 if (db_ok or not request.db) else 503
    return self._json_response(payload, status_code)

  # ── Auth ──────────────────────────────────────────────────────────

  @http.route('/api/v1/auth/login', type='http', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
  def auth_login(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    try:
      body = json.loads(request.httprequest.data or '{}')
      login = body.get('email') or body.get('login')
      password = body.get('password')
      db = body.get('db') or request.db
      if not all([login, password, db]):
        return self._json_response({'status': 'error', 'message': 'email, password, and db are required'}, 400)
      uid = request.session.authenticate(db, login, password)
      if not uid:
        return self._json_response({'status': 'error', 'message': 'Invalid credentials'}, 401)
      user = request.env['res.users'].sudo().browse(uid)
      registration = request.env['student.registration'].sudo().search([('user_id', '=', uid)], limit=1)
      return self._json_response({
        'status': 'success',
        'data': {
          'uid': uid,
          'name': user.name,
          'email': user.login,
          'session_id': request.session.sid,
          'registration_id': registration.id if registration else None,
        },
      })
    except AccessDenied:
      return self._json_response({'status': 'error', 'message': 'Invalid credentials'}, 401)
    except Exception as exc:
      _logger.exception('Login error')
      return self._json_response({'status': 'error', 'message': str(exc)}, 500)

  @http.route('/api/v1/auth/logout', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False)
  def auth_logout(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    request.session.logout()
    return self._json_response({'status': 'success', 'message': 'Logged out'})

  @http.route('/api/v1/auth/me', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False)
  def auth_me(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    user = request.env.user
    registration = request.env['student.registration'].search([('user_id', '=', user.id)], limit=1)
    return self._json_response({
      'status': 'success',
      'data': {
        'uid': user.id,
        'name': user.name,
        'email': user.login,
        'registration_id': registration.id if registration else None,
        'registration_number': registration.name if registration else None,
      },
    })

  # ── Public: Courses ───────────────────────────────────────────────

  @http.route('/api/v1/courses', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
  def list_courses(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    courses = request.env['student.course'].sudo().search([('active', '=', True)])
    data = [{
      'id': c.id,
      'name': c.name,
      'code': c.code,
      'department': c.department_id.name,
      'program': c.program_id.name,
      'campus': c.campus_id.name,
      'duration_months': c.duration_months,
      'total_seats': c.total_seats,
      'available_seats': c.available_seats,
      'admission_fee': c.admission_fee,
      'course_fee': c.course_fee,
      'eligibility_criteria': c.eligibility_criteria or '',
    } for c in courses]
    return self._json_response({'status': 'success', 'data': data})

  @http.route('/api/v1/academic-years', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
  def list_academic_years(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    years = request.env['student.academic.year'].sudo().search([('active', '=', True)])
    data = [{'id': y.id, 'name': y.name, 'code': y.code, 'current': y.current} for y in years]
    return self._json_response({'status': 'success', 'data': data})

  # ── Registration ──────────────────────────────────────────────────

  @http.route('/api/v1/registrations', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
  def create_registration(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    try:
      body = json.loads(request.httprequest.data or '{}')
      required = [
        'first_name', 'last_name', 'email', 'mobile', 'date_of_birth',
        'gender', 'address', 'parent_name', 'parent_mobile',
      ]
      missing = [f for f in required if not body.get(f)]
      if missing:
        return self._json_response({'status': 'error', 'message': 'Missing: %s' % ', '.join(missing)}, 400)
      Registration = request.env['student.registration'].sudo()
      registration = Registration.create(body)
      return self._json_response({
        'status': 'success',
        'data': {
          'id': registration.id,
          'registration_number': registration.name,
          'state': registration.state,
        },
      }, 201)
    except Exception as exc:
      _logger.exception('Registration error')
      return self._json_response({'status': 'error', 'message': str(exc)}, 400)

  @http.route('/api/v1/registrations/<int:reg_id>', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False)
  def get_registration(self, reg_id, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    reg = request.env['student.registration'].browse(reg_id)
    if not reg.exists():
      return self._json_response({'status': 'error', 'message': 'Not found'}, 404)
    return self._json_response({'status': 'success', 'data': self._serialize_registration(reg)})

  def _serialize_registration(self, reg):
    return {
      'id': reg.id,
      'registration_number': reg.name,
      'full_name': reg.full_name,
      'email': reg.email,
      'mobile': reg.mobile,
      'state': reg.state,
      'date_of_birth': str(reg.date_of_birth) if reg.date_of_birth else None,
      'gender': reg.gender,
      'address': reg.address,
      'parent_name': reg.parent_name,
      'parent_mobile': reg.parent_mobile,
    }

  # ── Admissions ────────────────────────────────────────────────────

  @http.route('/api/v1/admissions', type='http', auth='user', methods=['GET', 'POST', 'OPTIONS'], csrf=False)
  def admissions(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    if request.httprequest.method == 'POST':
      return self._create_admission()
    admissions = request.env['student.admission.application'].search([])
    return self._json_response({
      'status': 'success',
      'data': [self._serialize_admission(a) for a in admissions],
    })

  def _create_admission(self):
    try:
      body = json.loads(request.httprequest.data or '{}')
      required = ['registration_id', 'academic_year_id', 'course_id']
      missing = [f for f in required if not body.get(f)]
      if missing:
        return self._json_response({'status': 'error', 'message': 'Missing: %s' % ', '.join(missing)}, 400)
      admission = request.env['student.admission.application'].create(body)
      if body.get('auto_submit'):
        admission.action_submit()
      return self._json_response({'status': 'success', 'data': self._serialize_admission(admission)}, 201)
    except Exception as exc:
      return self._json_response({'status': 'error', 'message': str(exc)}, 400)

  @http.route('/api/v1/admissions/<int:adm_id>', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False)
  def get_admission(self, adm_id, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    admission = request.env['student.admission.application'].browse(adm_id)
    if not admission.exists():
      return self._json_response({'status': 'error', 'message': 'Not found'}, 404)
    data = self._serialize_admission(admission)
    data['documents'] = [{
      'id': d.id,
      'name': d.name,
      'state': d.state,
      'required': d.required,
      'remarks': d.remarks or '',
    } for d in admission.document_verification_ids]
    data['fees'] = [{
      'id': f.id,
      'receipt_number': f.name,
      'fee_type': f.fee_type,
      'amount': f.amount,
      'state': f.state,
      'due_date': str(f.due_date) if f.due_date else None,
      'payment_date': str(f.payment_date) if f.payment_date else None,
    } for f in admission.fee_ids]
    return self._json_response({'status': 'success', 'data': data})

  def _serialize_admission(self, a):
    return {
      'id': a.id,
      'admission_number': a.name,
      'student_name': a.full_name,
      'email': a.email,
      'state': a.state,
      'course': a.course_id.name,
      'course_id': a.course_id.id,
      'department': a.department_id.name,
      'campus': a.campus_id.name,
      'academic_year': a.academic_year_id.name,
      'merit_score': a.merit_score,
      'is_eligible': a.is_eligible,
      'total_fee': a.total_fee,
      'paid_fee': a.paid_fee,
      'pending_fee': a.pending_fee,
      'verification_progress': a.verification_progress,
      'application_date': str(a.application_date) if a.application_date else None,
    }

  # ── Fees ──────────────────────────────────────────────────────────

  @http.route('/api/v1/fees', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False)
  def list_fees(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    domain = []
    admission_id = kwargs.get('admission_id')
    if admission_id:
      domain.append(('admission_id', '=', int(admission_id)))
    fees = request.env['student.fee.payment'].search(domain)
    data = [{
      'id': f.id,
      'receipt_number': f.name,
      'student_name': f.student_name,
      'fee_type': f.fee_type,
      'amount': f.amount,
      'discount_amount': f.discount_amount,
      'scholarship_amount': f.scholarship_amount,
      'net_amount': f.net_amount,
      'state': f.state,
      'due_date': str(f.due_date) if f.due_date else None,
      'payment_date': str(f.payment_date) if f.payment_date else None,
    } for f in fees]
    return self._json_response({'status': 'success', 'data': data})

  # ── Dashboard ─────────────────────────────────────────────────────

  @http.route('/api/v1/dashboard', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False)
  def dashboard(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    Admission = request.env['student.admission.application']
    Registration = request.env['student.registration']
    Fee = request.env['student.fee.payment']
    dept_data = []
    for dept in request.env['student.department'].search([]):
      count = Admission.search_count([('department_id', '=', dept.id), ('state', '=', 'admitted')])
      dept_data.append({'department': dept.name, 'admissions': count})
    course_data = []
    for course in request.env['student.course'].search([]):
      count = Admission.search_count([('course_id', '=', course.id)])
      course_data.append({'course': course.name, 'applications': count})
    return self._json_response({
      'status': 'success',
      'data': {
        'total_students': Registration.search_count([('state', '=', 'registered')]),
        'total_applications': Admission.search_count([]),
        'pending_admissions': Admission.search_count([('state', 'in', ['submitted', 'under_review', 'verified'])]),
        'approved_admissions': Admission.search_count([('state', '=', 'approved')]),
        'rejected_admissions': Admission.search_count([('state', '=', 'rejected')]),
        'admitted_students': Admission.search_count([('state', '=', 'admitted')]),
        'fee_collected': sum(Fee.search([('state', '=', 'paid')]).mapped('net_amount')),
        'fee_pending': sum(Fee.search([('state', '=', 'pending')]).mapped('net_amount')),
        'department_wise': dept_data,
        'course_wise': course_data,
      },
    })

  # ── Contact ───────────────────────────────────────────────────────

  @http.route('/api/v1/contact', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
  def contact(self, **kwargs):
    opts = self._handle_options()
    if opts:
      return opts
    body = json.loads(request.httprequest.data or '{}')
    _logger.info('Contact form: %s', body)
    return self._json_response({'status': 'success', 'message': 'Thank you. We will contact you soon.'})
