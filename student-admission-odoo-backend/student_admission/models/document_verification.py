# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class StudentDocumentChecklist(models.Model):
  _name = 'student.document.checklist'
  _description = 'Document Checklist'
  _order = 'sequence, name'

  name = fields.Char(required=True)
  code = fields.Char(required=True)
  sequence = fields.Integer(default=10)
  required = fields.Boolean(default=True)
  description = fields.Text()
  active = fields.Boolean(default=True)

  _sql_constraints = [
    ('code_uniq', 'unique(code)', 'Document checklist code must be unique!'),
  ]


class StudentDocumentVerification(models.Model):
  _name = 'student.document.verification'
  _description = 'Document Verification'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'sequence, id'

  name = fields.Char(required=True, tracking=True)
  admission_id = fields.Many2one(
    'student.admission.application',
    required=True,
    ondelete='cascade',
    tracking=True,
  )
  checklist_id = fields.Many2one('student.document.checklist', ondelete='set null')
  sequence = fields.Integer(related='checklist_id.sequence', store=True)
  required = fields.Boolean(default=True)
  state = fields.Selection([
    ('pending', 'Pending'),
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
  ], default='pending', tracking=True, required=True)
  document_file = fields.Binary(string='Document', attachment=True)
  document_filename = fields.Char()
  verified_by = fields.Many2one('res.users', string='Verified By', readonly=True)
  verification_date = fields.Datetime(readonly=True)
  remarks = fields.Text(tracking=True)
  registration_id = fields.Many2one(
    'student.registration',
    related='admission_id.registration_id',
    store=True,
  )
  student_name = fields.Char(related='admission_id.full_name', store=True)

  def action_submit_document(self):
    for record in self:
      if not record.document_file:
        raise UserError('Please upload a document before submitting.')
      record.state = 'submitted'

  def action_approve(self):
    for record in self:
      record.write({
        'state': 'approved',
        'verified_by': self.env.user.id,
        'verification_date': fields.Datetime.now(),
      })

  def action_reject(self):
    self.ensure_one()
    return {
      'type': 'ir.actions.act_window',
      'name': 'Reject Document',
      'res_model': 'student.document.reject.wizard',
      'view_mode': 'form',
      'target': 'new',
      'context': {'default_verification_id': self.id},
    }
