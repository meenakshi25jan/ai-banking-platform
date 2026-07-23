# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentAdmissionDashboard(models.TransientModel):
  _name = 'student.admission.dashboard'
  _description = 'Admission Dashboard'

  total_applications = fields.Integer(compute='_compute_statistics')
  pending_applications = fields.Integer(compute='_compute_statistics')
  approved_applications = fields.Integer(compute='_compute_statistics')
  rejected_applications = fields.Integer(compute='_compute_statistics')
  admitted_applications = fields.Integer(compute='_compute_statistics')
  total_registrations = fields.Integer(compute='_compute_statistics')
  total_fee_collected = fields.Monetary(compute='_compute_statistics')
  total_fee_pending = fields.Monetary(compute='_compute_statistics')
  currency_id = fields.Many2one(
    'res.currency',
    default=lambda self: self.env.company.currency_id,
  )

  @api.depends_context('uid')
  def _compute_statistics(self):
    Admission = self.env['student.admission.application']
    Registration = self.env['student.registration']
    Fee = self.env['student.fee.payment']
    for dashboard in self:
      dashboard.total_applications = Admission.search_count([])
      dashboard.pending_applications = Admission.search_count([
        ('state', 'in', ['submitted', 'under_review']),
      ])
      dashboard.approved_applications = Admission.search_count([
        ('state', '=', 'approved'),
      ])
      dashboard.rejected_applications = Admission.search_count([
        ('state', '=', 'rejected'),
      ])
      dashboard.admitted_applications = Admission.search_count([
        ('state', '=', 'admitted'),
      ])
      dashboard.total_registrations = Registration.search_count([
        ('state', '=', 'registered'),
      ])
      paid_fees = Fee.search([('state', '=', 'paid')])
      pending_fees = Fee.search([('state', '=', 'pending')])
      dashboard.total_fee_collected = sum(paid_fees.mapped('net_amount'))
      dashboard.total_fee_pending = sum(pending_fees.mapped('net_amount'))

  def action_view_applications(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Applications',
      'res_model': 'student.admission.application',
      'view_mode': 'tree,form',
    }

  def action_view_pending(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Pending Applications',
      'res_model': 'student.admission.application',
      'view_mode': 'tree,form',
      'domain': [('state', 'in', ['submitted', 'under_review'])],
    }

  def action_view_approved(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Approved Applications',
      'res_model': 'student.admission.application',
      'view_mode': 'tree,form',
      'domain': [('state', '=', 'approved')],
    }

  def action_view_rejected(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Rejected Applications',
      'res_model': 'student.admission.application',
      'view_mode': 'tree,form',
      'domain': [('state', '=', 'rejected')],
    }

  def action_view_admitted(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Admitted Students',
      'res_model': 'student.admission.application',
      'view_mode': 'tree,form',
      'domain': [('state', '=', 'admitted')],
    }

  def action_view_fees(self):
    return {
      'type': 'ir.actions.act_window',
      'name': 'Fee Payments',
      'res_model': 'student.fee.payment',
      'view_mode': 'tree,form',
    }
