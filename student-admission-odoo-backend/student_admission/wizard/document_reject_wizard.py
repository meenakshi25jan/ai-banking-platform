# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentDocumentRejectWizard(models.TransientModel):
  _name = 'student.document.reject.wizard'
  _description = 'Document Rejection Wizard'

  verification_id = fields.Many2one(
    'student.document.verification',
    required=True,
  )
  remarks = fields.Text(required=True, string='Rejection Remarks')

  def action_confirm_reject(self):
    self.ensure_one()
    self.verification_id.write({
      'state': 'rejected',
      'remarks': self.remarks,
      'verified_by': self.env.user.id,
      'verification_date': fields.Datetime.now(),
    })
    return {'type': 'ir.actions.act_window_close'}
