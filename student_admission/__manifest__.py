# -*- coding: utf-8 -*-
{
  'name': 'Student Admission ERP',
  'version': '17.0.2.0.0',
  'category': 'Education',
  'summary': 'Student Registration and Admission Management System',
  'description': """
Student Admission ERP
=====================
Complete solution for student registration, admission workflows,
document verification, fee management, and reporting.

Features:
---------
* Student registration with unique registration numbers
* Admission application lifecycle (Draft → Admitted)
* Academic structure (Campus, Department, Program, Course, Semester, Batch)
* Document verification workflow
* Fee management with receipts
* Role-based security (Administrator, Officer, Account Officer, Student)
* Admission dashboard and comprehensive reports
* Email notifications for registration, approval, rejection, and fee reminders
  """,
  'author': 'Student Admission ERP',
  'website': 'https://www.odoo.com',
  'license': 'LGPL-3',
  'depends': [
    'base',
    'mail',
    'portal',
    'web',
  ],
  'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'data/sequence_data.xml',
    'data/document_checklist_data.xml',
    'data/mail_template_data.xml',
    'data/cron_data.xml',
    'views/campus_views.xml',
    'views/department_views.xml',
    'views/program_views.xml',
    'views/course_views.xml',
    'views/semester_views.xml',
    'views/batch_views.xml',
    'views/academic_year_views.xml',
    'views/student_registration_views.xml',
    'views/admission_application_views.xml',
    'views/document_verification_views.xml',
    'views/fee_views.xml',
    'views/scholarship_views.xml',
    'views/dashboard_views.xml',
    'wizard/document_reject_wizard_views.xml',
    'report/report_templates.xml',
    'report/admission_reports.xml',
    'views/menus.xml',
  ],
  'demo': [
    'demo/demo_data.xml',
    'demo/demo_users.xml',
  ],
  'assets': {},
  'installable': True,
  'application': True,
  'auto_install': False,
}
