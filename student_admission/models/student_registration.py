# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
  _name = 'student.registration'
  _description = 'Student Registration'
  _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
  _order = 'create_date desc'

  name = fields.Char(
    string='Registration Number',
    readonly=True,
    copy=False,
    default='New',
    tracking=True,
  )
  state = fields.Selection([
    ('draft', 'Draft'),
    ('registered', 'Registered'),
    ('cancelled', 'Cancelled'),
  ], default='draft', tracking=True, required=True)

  first_name = fields.Char(required=True, tracking=True)
  last_name = fields.Char(required=True, tracking=True)
  full_name = fields.Char(compute='_compute_full_name', store=True)
  date_of_birth = fields.Date(required=True, tracking=True)
  gender = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
  ], required=True, tracking=True)
  address = fields.Text(required=True)
  city = fields.Char()
  state_id = fields.Many2one('res.country.state', string='State')
  country_id = fields.Many2one('res.country', string='Country')
  zip = fields.Char(string='ZIP')
  mobile = fields.Char(required=True, tracking=True)
  email = fields.Char(required=True, tracking=True)
  aadhaar_number = fields.Char(string='Aadhaar/Identity Number', tracking=True)

  parent_name = fields.Char(string='Parent/Guardian Name', required=True)
  parent_relation = fields.Selection([
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('guardian', 'Guardian'),
    ('other', 'Other'),
  ], default='father', required=True)
  parent_mobile = fields.Char(string='Parent Mobile', required=True)
  parent_email = fields.Char(string='Parent Email')

  photograph = fields.Binary(string='Photograph', attachment=True)
  photograph_filename = fields.Char()
  document_ids = fields.One2many(
    'student.registration.document',
    'registration_id',
    string='Supporting Documents',
  )
  admission_ids = fields.One2many(
    'student.admission.application',
    'registration_id',
    string='Admission Applications',
  )
  admission_count = fields.Integer(compute='_compute_admission_count')
  user_id = fields.Many2one('res.users', string='Portal User', copy=False)
  company_id = fields.Many2one(
    'res.company',
    default=lambda self: self.env.company,
    required=True,
  )

  _sql_constraints = [
    ('aadhaar_uniq', 'unique(aadhaar_number)', 'Aadhaar/Identity number must be unique!'),
  ]

  @api.depends('first_name', 'last_name')
  def _compute_full_name(self):
    for record in self:
      record.full_name = ' '.join(filter(None, [record.first_name, record.last_name]))

  def _compute_admission_count(self):
    for record in self:
      record.admission_count = len(record.admission_ids)

  @api.constrains('email', 'parent_email')
  def _check_email_format(self):
    for record in self:
      if record.email and '@' not in record.email:
        raise ValidationError('Please provide a valid student email address.')
      if record.parent_email and '@' not in record.parent_email:
        raise ValidationError('Please provide a valid parent email address.')

  @api.model_create_multi
  def create(self, vals_list):
    for vals in vals_list:
      if vals.get('name', 'New') == 'New':
        vals['name'] = self.env['ir.sequence'].next_by_code('student.registration') or 'New'
    return super().create(vals_list)

  def action_register(self):
    for record in self:
      if record.state != 'draft':
        continue
      record.state = 'registered'
      record._send_registration_confirmation()

  def action_cancel(self):
    self.write({'state': 'cancelled'})

  def action_reset_draft(self):
    self.write({'state': 'draft'})

  def action_create_admission(self):
    self.ensure_one()
    return {
      'type': 'ir.actions.act_window',
      'name': 'Admission Application',
      'res_model': 'student.admission.application',
      'view_mode': 'form',
      'context': {
        'default_registration_id': self.id,
        'default_first_name': self.first_name,
        'default_last_name': self.last_name,
        'default_email': self.email,
        'default_mobile': self.mobile,
      },
    }

  def _send_registration_confirmation(self):
    template = self.env.ref(
      'student_admission.mail_template_registration_confirmation',
      raise_if_not_found=False,
    )
    if template:
      for record in self:
        template.send_mail(record.id, force_send=True)

  def _compute_access_url(self):
    super()._compute_access_url()
    for record in self:
      record.access_url = '/my/student/registration/%s' % record.id


class StudentRegistrationDocument(models.Model):
  _name = 'student.registration.document'
  _description = 'Student Registration Document'

  name = fields.Char(required=True)
  registration_id = fields.Many2one(
    'student.registration',
    required=True,
    ondelete='cascade',
  )
  document_type = fields.Selection([
    ('identity', 'Identity Proof'),
    ('address', 'Address Proof'),
    ('marksheet', 'Mark Sheet'),
    ('certificate', 'Certificate'),
    ('photo', 'Photograph'),
    ('other', 'Other'),
  ], default='other', required=True)
  file = fields.Binary(required=True, attachment=True)
  filename = fields.Char()
  description = fields.Text()
