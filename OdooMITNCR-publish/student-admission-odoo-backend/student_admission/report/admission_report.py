# -*- coding: utf-8 -*-
from odoo import models


class ReportStudentRegistration(models.AbstractModel):
  _name = 'report.student_admission.report_student_registration'
  _description = 'Student Registration Report'

  def _get_report_values(self, docids, data=None):
    docs = self.env['student.registration'].browse(docids)
    return {
      'doc_ids': docids,
      'doc_model': 'student.registration',
      'docs': docs,
    }


class ReportAdmissionSummary(models.AbstractModel):
  _name = 'report.student_admission.report_admission_summary'
  _description = 'Admission Summary Report'

  def _get_report_values(self, docids, data=None):
    docs = self.env['student.admission.application'].browse(docids)
    return {
      'doc_ids': docids,
      'doc_model': 'student.admission.application',
      'docs': docs,
    }


class ReportFeeCollection(models.AbstractModel):
  _name = 'report.student_admission.report_fee_collection'
  _description = 'Fee Collection Report'

  def _get_report_values(self, docids, data=None):
    docs = self.env['student.fee.payment'].browse(docids)
    return {
      'doc_ids': docids,
      'doc_model': 'student.fee.payment',
      'docs': docs,
    }
