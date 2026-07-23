# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentProgram(models.Model):
  _name = 'student.program'
  _description = 'Academic Program'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'name'

  name = fields.Char(required=True, tracking=True)
  code = fields.Char(required=True, tracking=True)
  department_id = fields.Many2one('student.department', required=True, ondelete='restrict')
  campus_id = fields.Many2one(
    'student.campus',
    related='department_id.campus_id',
    store=True,
    readonly=True,
  )
  duration_years = fields.Float(string='Duration (Years)', default=3.0)
  description = fields.Text()
  active = fields.Boolean(default=True)
  course_ids = fields.One2many('student.course', 'program_id', string='Courses')

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Program code must be unique!'),
  ]
