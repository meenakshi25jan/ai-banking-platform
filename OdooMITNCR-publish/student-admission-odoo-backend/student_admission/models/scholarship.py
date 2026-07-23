# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentScholarship(models.Model):
  _name = 'student.scholarship'
  _description = 'Scholarship'
  _order = 'name'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  scholarship_type = fields.Selection([
    ('merit', 'Merit Based'),
    ('need', 'Need Based'),
    ('sports', 'Sports'),
    ('other', 'Other'),
  ], default='merit', required=True)
  amount = fields.Monetary(string='Scholarship Amount')
  percentage = fields.Float(string='Discount %', help='Percentage off total fee')
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )
  active = fields.Boolean(default=True)
  description = fields.Text()

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Scholarship code must be unique!'),
  ]

  @api.constrains('percentage')
  def _check_percentage(self):
    for record in self:
      if record.percentage < 0 or record.percentage > 100:
        raise ValidationError('Scholarship percentage must be between 0 and 100.')


class StudentDiscount(models.Model):
  _name = 'student.discount'
  _description = 'Fee Discount'
  _order = 'name'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  discount_type = fields.Selection([
    ('fixed', 'Fixed Amount'),
    ('percentage', 'Percentage'),
  ], default='percentage', required=True)
  amount = fields.Monetary()
  percentage = fields.Float()
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )
  active = fields.Boolean(default=True)

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Discount code must be unique!'),
  ]
