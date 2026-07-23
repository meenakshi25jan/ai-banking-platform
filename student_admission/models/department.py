# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentDepartment(models.Model):
  _name = 'student.department'
  _description = 'Department'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'name'

  name = fields.Char(required=True, tracking=True)
  code = fields.Char(required=True, tracking=True)
  campus_id = fields.Many2one('student.campus', required=True, ondelete='restrict')
  head_id = fields.Many2one('res.users', string='Department Head')
  description = fields.Text()
  active = fields.Boolean(default=True)
  program_ids = fields.One2many('student.program', 'department_id', string='Programs')

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Department code must be unique!'),
  ]
