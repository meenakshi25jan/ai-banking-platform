# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentBatch(models.Model):
  _name = 'student.batch'
  _description = 'Student Batch'
  _order = 'name desc'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  course_id = fields.Many2one('student.course', required=True, ondelete='restrict')
  academic_year_id = fields.Many2one('student.academic.year', required=True, ondelete='restrict')
  start_date = fields.Date()
  end_date = fields.Date()
  capacity = fields.Integer(default=60)
  active = fields.Boolean(default=True)
  student_count = fields.Integer(compute='_compute_student_count')

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Batch code must be unique!'),
  ]

  def _compute_student_count(self):
    Admission = self.env['student.admission.application']
    for batch in self:
      batch.student_count = Admission.search_count([
        ('batch_id', '=', batch.id),
        ('state', '=', 'admitted'),
      ])
