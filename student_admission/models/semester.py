# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentSemester(models.Model):
  _name = 'student.semester'
  _description = 'Semester'
  _order = 'sequence, name'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  sequence = fields.Integer(default=1)
  program_id = fields.Many2one('student.program', ondelete='restrict')
  academic_year_id = fields.Many2one('student.academic.year', ondelete='restrict')
  date_start = fields.Date()
  date_end = fields.Date()
  active = fields.Boolean(default=True)

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Semester code must be unique!'),
  ]
