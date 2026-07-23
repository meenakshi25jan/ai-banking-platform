# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentCourse(models.Model):
  _name = 'student.course'
  _description = 'Course'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'name'

  name = fields.Char(required=True, tracking=True)
  code = fields.Char(required=True, tracking=True)
  program_id = fields.Many2one('student.program', required=True, ondelete='restrict')
  department_id = fields.Many2one(
    'student.department',
    related='program_id.department_id',
    store=True,
    readonly=True,
  )
  campus_id = fields.Many2one(
    'student.campus',
    related='program_id.campus_id',
    store=True,
    readonly=True,
  )
  duration_months = fields.Integer(string='Duration (Months)', default=36)
  total_seats = fields.Integer(string='Total Seats', default=60)
  min_merit_score = fields.Float(
    string='Minimum Merit Score',
    default=0.0,
    help='Minimum merit score required for admission eligibility.',
  )
  admission_fee = fields.Monetary(string='Admission Fee', currency_field='currency_id')
  course_fee = fields.Monetary(string='Course Fee', currency_field='currency_id')
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )
  eligibility_criteria = fields.Text()
  description = fields.Text()
  active = fields.Boolean(default=True)
  admission_count = fields.Integer(compute='_compute_admission_count')
  available_seats = fields.Integer(compute='_compute_available_seats')

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Course code must be unique!'),
    ('total_seats_positive', 'CHECK(total_seats >= 0)', 'Total seats cannot be negative.'),
  ]

  @api.depends('admission_count')
  def _compute_admission_count(self):
    Admission = self.env['student.admission.application']
    for course in self:
      course.admission_count = Admission.search_count([
        ('course_id', '=', course.id),
        ('state', 'in', ['approved', 'admitted']),
      ])

  @api.depends('total_seats', 'admission_count')
  def _compute_available_seats(self):
    for course in self:
      course.available_seats = max(course.total_seats - course.admission_count, 0)

  @api.constrains('admission_fee', 'course_fee')
  def _check_fees(self):
    for record in self:
      if record.admission_fee < 0 or record.course_fee < 0:
        raise ValidationError('Fees cannot be negative.')
