# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentAcademicYear(models.Model):
  _name = 'student.academic.year'
  _description = 'Academic Year'
  _order = 'date_start desc'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  date_start = fields.Date(required=True)
  date_end = fields.Date(required=True)
  active = fields.Boolean(default=True)
  current = fields.Boolean(string='Current Year', default=False)

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Academic year code must be unique!'),
  ]

  @api.constrains('date_start', 'date_end')
  def _check_dates(self):
    for record in self:
      if record.date_start and record.date_end and record.date_start >= record.date_end:
        raise ValidationError('Academic year start date must be before end date.')

  @api.constrains('current')
  def _check_single_current(self):
    for record in self.filtered('current'):
      others = self.search([
        ('current', '=', True),
        ('id', '!=', record.id),
      ])
      if others:
        raise ValidationError('Only one academic year can be marked as current.')
