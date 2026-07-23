# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestStudentRegistration(TransactionCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.Campus = cls.env['student.campus']
    cls.Department = cls.env['student.department']
    cls.Program = cls.env['student.program']
    cls.Course = cls.env['student.course']
    cls.AcademicYear = cls.env['student.academic.year']
    cls.Registration = cls.env['student.registration']

    cls.campus = cls.Campus.create({
      'name': 'Test Campus',
      'code': 'TC-01',
    })
    cls.department = cls.Department.create({
      'name': 'Test Department',
      'code': 'TD-01',
      'campus_id': cls.campus.id,
    })
    cls.program = cls.Program.create({
      'name': 'Test Program',
      'code': 'TP-01',
      'department_id': cls.department.id,
    })
    cls.course = cls.Course.create({
      'name': 'Test Course',
      'code': 'TC-101',
      'program_id': cls.program.id,
      'total_seats': 10,
      'admission_fee': 1000,
      'course_fee': 5000,
    })
    cls.academic_year = cls.AcademicYear.create({
      'name': '2025-2026',
      'code': 'AY-TEST',
      'date_start': '2025-07-01',
      'date_end': '2026-06-30',
    })

  def _create_registration(self, **kwargs):
    values = {
      'first_name': 'Test',
      'last_name': 'Student',
      'date_of_birth': '2005-01-01',
      'gender': 'male',
      'address': 'Test Address',
      'mobile': '9000000001',
      'email': 'test.student@example.com',
      'parent_name': 'Parent Name',
      'parent_mobile': '9000000002',
      'aadhaar_number': '111122223333',
    }
    values.update(kwargs)
    return self.Registration.create(values)

  def test_registration_sequence_generation(self):
    registration = self._create_registration(aadhaar_number='444455556666')
    self.assertNotEqual(registration.name, 'New')
    self.assertTrue(registration.name.startswith('REG/'))

  def test_registration_workflow(self):
    registration = self._create_registration(aadhaar_number='777788889999')
    self.assertEqual(registration.state, 'draft')
    registration.action_register()
    self.assertEqual(registration.state, 'registered')

  def test_full_name_compute(self):
    registration = self._create_registration(
      first_name='John',
      last_name='Doe',
      aadhaar_number='121212121212',
    )
    self.assertEqual(registration.full_name, 'John Doe')


@tagged('post_install', '-at_install')
class TestAdmissionApplication(TransactionCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.env = cls.env

    cls.campus = cls.env['student.campus'].create({'name': 'Campus', 'code': 'C1'})
    cls.department = cls.env['student.department'].create({
      'name': 'Dept', 'code': 'D1', 'campus_id': cls.campus.id,
    })
    cls.program = cls.env['student.program'].create({
      'name': 'Program', 'code': 'P1', 'department_id': cls.department.id,
    })
    cls.course = cls.env['student.course'].create({
      'name': 'Course', 'code': 'CR1', 'program_id': cls.program.id,
      'total_seats': 5, 'admission_fee': 500, 'course_fee': 2000,
    })
    cls.academic_year = cls.env['student.academic.year'].create({
      'name': '2025-2026', 'code': 'AY1',
      'date_start': '2025-07-01', 'date_end': '2026-06-30',
    })
    cls.registration = cls.env['student.registration'].create({
      'first_name': 'Ada', 'last_name': 'Lovelace',
      'date_of_birth': '2004-06-01', 'gender': 'female',
      'address': 'London', 'mobile': '9111111111',
      'email': 'ada@example.com', 'parent_name': 'Parent',
      'parent_mobile': '9222222222', 'aadhaar_number': '999988887777',
      'state': 'registered',
    })

  def test_admission_workflow(self):
    admission = self.env['student.admission.application'].create({
      'registration_id': self.registration.id,
      'academic_year_id': self.academic_year.id,
      'course_id': self.course.id,
    })
    self.assertNotEqual(admission.name, 'New')
    self.assertTrue(admission.document_verification_ids)

    admission.action_submit()
    self.assertEqual(admission.state, 'submitted')

    for doc in admission.document_verification_ids:
      doc.write({'document_file': b'test', 'document_filename': 'test.pdf'})
      doc.action_submit_document()
      doc.action_approve()

    admission.action_under_review()
    admission.action_approve()
    self.assertEqual(admission.state, 'approved')
    self.assertTrue(admission.fee_ids)

    for fee in admission.fee_ids:
      fee.write({'payment_method': 'cash'})
      fee.action_register_payment()

    admission.action_admit()
    self.assertEqual(admission.state, 'admitted')


@tagged('post_install', '-at_install')
class TestCourseManagement(TransactionCase):

  def test_available_seats(self):
    campus = self.env['student.campus'].create({'name': 'C', 'code': 'C2'})
    department = self.env['student.department'].create({
      'name': 'D', 'code': 'D2', 'campus_id': campus.id,
    })
    program = self.env['student.program'].create({
      'name': 'P', 'code': 'P2', 'department_id': department.id,
    })
    course = self.env['student.course'].create({
      'name': 'Course', 'code': 'CR2', 'program_id': program.id, 'total_seats': 2,
    })
    self.assertEqual(course.available_seats, 2)

  def test_academic_year_date_validation(self):
    with self.assertRaises(ValidationError):
      self.env['student.academic.year'].create({
        'name': 'Invalid', 'code': 'INV',
        'date_start': '2026-01-01', 'date_end': '2025-01-01',
      })
