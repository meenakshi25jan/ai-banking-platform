# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class StudentAdmissionApplication(models.Model):
  _name = 'student.admission.application'
  _description = 'Admission Application'
  _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
  _order = 'create_date desc'

  name = fields.Char(
    string='Admission Number',
    readonly=True,
    copy=False,
    default='New',
    tracking=True,
  )
  state = fields.Selection([
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('under_review', 'Under Review'),
    ('verified', 'Verified'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('admitted', 'Admitted'),
  ], default='draft', tracking=True, required=True, index=True)

  registration_id = fields.Many2one(
    'student.registration',
    required=True,
    ondelete='restrict',
    tracking=True,
  )
  full_name = fields.Char(related='registration_id.full_name', store=True)
  email = fields.Char(related='registration_id.email', store=True)
  mobile = fields.Char(related='registration_id.mobile', store=True)

  academic_year_id = fields.Many2one(
    'student.academic.year',
    required=True,
    tracking=True,
  )
  course_id = fields.Many2one('student.course', required=True, tracking=True)
  program_id = fields.Many2one(
    'student.program',
    related='course_id.program_id',
    store=True,
    readonly=True,
  )
  department_id = fields.Many2one(
    'student.department',
    related='course_id.department_id',
    store=True,
    readonly=True,
  )
  campus_id = fields.Many2one(
    'student.campus',
    related='course_id.campus_id',
    store=True,
    readonly=True,
  )
  batch_id = fields.Many2one('student.batch', tracking=True)
  semester_id = fields.Many2one('student.semester')

  application_date = fields.Date(
    default=fields.Date.context_today,
    required=True,
    tracking=True,
  )
  review_date = fields.Date(tracking=True)
  admission_date = fields.Date(tracking=True)
  rejection_reason = fields.Text(tracking=True)
  merit_score = fields.Float(string='Merit Score', tracking=True)
  is_eligible = fields.Boolean(string='Eligible', compute='_compute_eligibility', store=True)
  scholarship_id = fields.Many2one('student.scholarship', string='Scholarship', tracking=True)
  discount_id = fields.Many2one('student.discount', string='Discount', tracking=True)

  document_verification_ids = fields.One2many(
    'student.document.verification',
    'admission_id',
    string='Document Verifications',
  )
  fee_ids = fields.One2many('student.fee.payment', 'admission_id', string='Fee Payments')
  total_fee = fields.Monetary(compute='_compute_fee_totals', store=True)
  paid_fee = fields.Monetary(compute='_compute_fee_totals', store=True)
  pending_fee = fields.Monetary(compute='_compute_fee_totals', store=True)
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )
  company_id = fields.Many2one(
    'res.company',
    default=lambda self: self.env.company,
    required=True,
  )
  verification_progress = fields.Float(compute='_compute_verification_progress')
  all_documents_verified = fields.Boolean(compute='_compute_verification_progress')

  @api.depends('fee_ids.amount', 'fee_ids.state', 'fee_ids.net_amount', 'course_id', 'scholarship_id', 'discount_id')
  def _compute_fee_totals(self):
    for record in self:
      base = (record.course_id.admission_fee or 0.0) + (record.course_id.course_fee or 0.0)
      scholarship_amt = 0.0
      if record.scholarship_id:
        if record.scholarship_id.percentage:
          scholarship_amt = base * (record.scholarship_id.percentage / 100)
        else:
          scholarship_amt = record.scholarship_id.amount or 0.0
      discount_amt = 0.0
      if record.discount_id:
        if record.discount_id.discount_type == 'percentage':
          discount_amt = base * ((record.discount_id.percentage or 0) / 100)
        else:
          discount_amt = record.discount_id.amount or 0.0
      total = max(base - scholarship_amt - discount_amt, 0.0)
      paid = sum(record.fee_ids.filtered(lambda f: f.state == 'paid').mapped('net_amount'))
      record.total_fee = total
      record.paid_fee = paid
      record.pending_fee = max(total - paid, 0.0)

  @api.depends('document_verification_ids.state', 'document_verification_ids.required')
  def _compute_verification_progress(self):
    for record in self:
      docs = record.document_verification_ids
      required_docs = docs.filtered('required')
      if not required_docs:
        record.verification_progress = 100.0 if docs else 0.0
        record.all_documents_verified = not docs or all(d.state == 'approved' for d in docs)
        continue
      approved = len(required_docs.filtered(lambda d: d.state == 'approved'))
      record.verification_progress = (approved / len(required_docs)) * 100
      record.all_documents_verified = all(d.state == 'approved' for d in required_docs)

  @api.model_create_multi
  def create(self, vals_list):
    for vals in vals_list:
      if vals.get('name', 'New') == 'New':
        vals['name'] = self.env['ir.sequence'].next_by_code('student.admission') or 'New'
    records = super().create(vals_list)
    for record in records:
      record._create_document_checklist()
    return records

  def _create_document_checklist(self):
    Checklist = self.env['student.document.checklist']
    Verification = self.env['student.document.verification']
    for record in self:
      checklists = Checklist.search([('active', '=', True)])
      for checklist in checklists:
        Verification.create({
          'admission_id': record.id,
          'checklist_id': checklist.id,
          'name': checklist.name,
          'required': checklist.required,
        })

  def action_submit(self):
    for record in self:
      if record.state != 'draft':
        raise UserError('Only draft applications can be submitted.')
      if not record.document_verification_ids:
        record._create_document_checklist()
      record.state = 'submitted'
      record._send_submission_email()

  @api.depends('merit_score', 'course_id.min_merit_score')
  def _compute_eligibility(self):
    for record in self:
      minimum = record.course_id.min_merit_score if record.course_id else 0.0
      record.is_eligible = (record.merit_score or 0.0) >= minimum

  def action_verify(self):
    for record in self:
      if record.state != 'under_review':
        raise UserError('Only under-review applications can be verified.')
      if record.document_verification_ids and not record.all_documents_verified:
        raise ValidationError('All required documents must be verified first.')
      record.state = 'verified'

  def action_under_review(self):
    self.write({'state': 'under_review', 'review_date': fields.Date.today()})

  def action_approve(self):
    for record in self:
      if record.state not in ('submitted', 'under_review', 'verified'):
        raise UserError('Only submitted, under-review, or verified applications can be approved.')
      if record.course_id.available_seats <= 0:
        raise ValidationError('No seats available for the selected course.')
      if not record.is_eligible:
        raise ValidationError(
          'Student does not meet the minimum merit score for this course.',
        )
      if record.document_verification_ids and not record.all_documents_verified:
        raise ValidationError('All required documents must be verified before approval.')
      record.state = 'approved'
      record._send_approval_email()
      record._create_fee_lines()

  def action_reject(self):
    self.ensure_one()
    return {
      'type': 'ir.actions.act_window',
      'name': 'Reject Admission',
      'res_model': 'student.admission.reject.wizard',
      'view_mode': 'form',
      'target': 'new',
      'context': {'default_admission_id': self.id},
    }

  def action_admit(self):
    for record in self:
      if record.state != 'approved':
        raise UserError('Only approved applications can be admitted.')
      if record.pending_fee > 0:
        raise ValidationError('All fees must be paid before admission.')
      record.state = 'admitted'
      record.admission_date = fields.Date.today()
      record._send_admission_complete_email()
      if not record.batch_id:
        batch = self.env['student.batch'].search([
          ('course_id', '=', record.course_id.id),
          ('academic_year_id', '=', record.academic_year_id.id),
        ], limit=1)
        if batch:
          record.batch_id = batch.id

  def action_reset_draft(self):
    self.write({'state': 'draft'})

  def _create_fee_lines(self):
    FeePayment = self.env['student.fee.payment']
    for record in self:
      if record.fee_ids:
        continue
      base = (record.course_id.admission_fee or 0.0) + (record.course_id.course_fee or 0.0)
      scholarship_amt = 0.0
      if record.scholarship_id:
        if record.scholarship_id.percentage:
          scholarship_amt = base * (record.scholarship_id.percentage / 100)
        else:
          scholarship_amt = record.scholarship_id.amount or 0.0
      discount_amt = 0.0
      if record.discount_id:
        if record.discount_id.discount_type == 'percentage':
          discount_amt = base * ((record.discount_id.percentage or 0) / 100)
        else:
          discount_amt = record.discount_id.amount or 0.0
      total_adjustment = scholarship_amt + discount_amt
      lines = []
      if record.course_id.admission_fee:
        lines.append(('admission', record.course_id.admission_fee))
      if record.course_id.course_fee:
        lines.append(('course', record.course_id.course_fee))
      for fee_type, amount in lines:
        share = (amount / base) if base else 0.0
        FeePayment.create({
          'admission_id': record.id,
          'fee_type': fee_type,
          'amount': amount,
          'scholarship_amount': scholarship_amt * share,
          'discount_amount': discount_amt * share,
          'due_date': (
            fields.Date.today()
            if fee_type == 'admission'
            else fields.Date.today() + relativedelta(months=1)
          ),
        })

  def _send_approval_email(self):
    template = self.env.ref(
      'student_admission.mail_template_admission_approval',
      raise_if_not_found=False,
    )
    if template:
      template.send_mail(self.id, force_send=True)

  def _send_rejection_email(self):
    template = self.env.ref(
      'student_admission.mail_template_admission_rejection',
      raise_if_not_found=False,
    )
    if template:
      template.send_mail(self.id, force_send=True)

  def _send_submission_email(self):
    template = self.env.ref(
      'student_admission.mail_template_admission_submitted',
      raise_if_not_found=False,
    )
    if template:
      template.send_mail(self.id, force_send=True)

  def _send_admission_complete_email(self):
    template = self.env.ref(
      'student_admission.mail_template_admission_complete',
      raise_if_not_found=False,
    )
    if template:
      template.send_mail(self.id, force_send=True)

  def _compute_access_url(self):
    super()._compute_access_url()
    for record in self:
      record.access_url = '/my/student/admission/%s' % record.id
