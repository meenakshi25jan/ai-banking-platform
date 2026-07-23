# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentCampus(models.Model):
  _name = 'student.campus'
  _description = 'Campus'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'name'

  name = fields.Char(required=True, tracking=True)
  code = fields.Char(required=True, tracking=True)
  address = fields.Text()
  city = fields.Char()
  state_id = fields.Many2one('res.country.state', string='State')
  country_id = fields.Many2one('res.country', string='Country')
  zip = fields.Char(string='ZIP')
  phone = fields.Char()
  email = fields.Char()
  active = fields.Boolean(default=True)
  department_ids = fields.One2many('student.department', 'campus_id', string='Departments')
  department_count = fields.Integer(compute='_compute_department_count')

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Campus code must be unique!'),
  ]

  @api.depends('department_ids')
  def _compute_department_count(self):
    for campus in self:
      campus.department_count = len(campus.department_ids)
