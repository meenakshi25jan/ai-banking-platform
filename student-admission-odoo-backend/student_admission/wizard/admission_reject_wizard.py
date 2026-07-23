# -*- coding: utf-8 -*-
from odoo import fields, models


class StudentAdmissionRejectWizard(models.TransientModel):
  _name = 'student.admission.reject.wizard'
  _description = 'Admission Rejection Wizard'

  admission_id = fields.Many2one(
    'student.admission.application',
    required=True,
  )
  rejection_reason = fields.Text(required=True)

  def action_confirm_reject(self):
    self.ensure_one()
    self.admission_id.write({
      'state': 'rejected',
      'rejection_reason': self.rejection_reason,
    })
    self.admission_id._send_rejection_email()
    return {'type': 'ir.actions.act_window_close'}
