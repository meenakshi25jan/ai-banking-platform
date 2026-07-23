# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class StudentFeePayment(models.Model):
  _name = 'student.fee.payment'
  _description = 'Student Fee Payment'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'due_date, id'

  name = fields.Char(
    string='Receipt Number',
    readonly=True,
    copy=False,
    default='New',
  )
  admission_id = fields.Many2one(
    'student.admission.application',
    required=True,
    ondelete='cascade',
    tracking=True,
  )
  registration_id = fields.Many2one(
    'student.registration',
    related='admission_id.registration_id',
    store=True,
  )
  student_name = fields.Char(related='admission_id.full_name', store=True)
  course_id = fields.Many2one(
    'student.course',
    related='admission_id.course_id',
    store=True,
  )
  fee_type = fields.Selection([
    ('admission', 'Admission Fee'),
    ('course', 'Course Fee'),
    ('other', 'Other'),
  ], required=True, tracking=True)
  amount = fields.Monetary(required=True, tracking=True)
  discount_amount = fields.Monetary(string='Discount', default=0.0)
  scholarship_amount = fields.Monetary(string='Scholarship', default=0.0)
  net_amount = fields.Monetary(compute='_compute_net_amount', store=True)
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )
  due_date = fields.Date(tracking=True)
  payment_date = fields.Date(tracking=True)
  payment_method = fields.Selection([
    ('cash', 'Cash'),
    ('bank', 'Bank Transfer'),
    ('card', 'Card'),
    ('upi', 'UPI'),
    ('cheque', 'Cheque'),
    ('online', 'Online'),
  ], tracking=True)
  reference = fields.Char(string='Payment Reference')
  state = fields.Selection([
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled'),
  ], default='pending', tracking=True, required=True)
  notes = fields.Text()
  company_id = fields.Many2one(
    'res.company',
    default=lambda self: self.env.company,
    required=True,
  )

  @api.depends('amount', 'discount_amount', 'scholarship_amount')
  def _compute_net_amount(self):
    for record in self:
      record.net_amount = max(
        (record.amount or 0) - (record.discount_amount or 0) - (record.scholarship_amount or 0),
        0.0,
      )

  @api.model_create_multi
  def create(self, vals_list):
    for vals in vals_list:
      if vals.get('name', 'New') == 'New':
        vals['name'] = self.env['ir.sequence'].next_by_code('student.fee.receipt') or 'New'
    return super().create(vals_list)

  def action_register_payment(self):
    for record in self:
      if record.state != 'pending':
        raise UserError('Only pending fees can be paid.')
      record.write({
        'state': 'paid',
        'payment_date': fields.Date.today(),
      })
      record._send_payment_confirmation_email()

  def _send_payment_confirmation_email(self):
    template = self.env.ref(
      'student_admission.mail_template_payment_received',
      raise_if_not_found=False,
    )
    if template:
      for record in self:
        template.send_mail(record.id, force_send=True)

  def action_cancel(self):
    self.write({'state': 'cancelled'})

  def action_reset_pending(self):
    self.write({
      'state': 'pending',
      'payment_date': False,
      'payment_method': False,
      'reference': False,
    })

  @api.model
  def _cron_send_fee_due_reminders(self):
    today = fields.Date.today()
    reminder_date = today + relativedelta(days=7)
    pending_fees = self.search([
      ('state', '=', 'pending'),
      ('due_date', '<=', reminder_date),
    ])
    template = self.env.ref(
      'student_admission.mail_template_fee_due_reminder',
      raise_if_not_found=False,
    )
    if template:
      for fee in pending_fees:
        template.send_mail(fee.id, force_send=False)
