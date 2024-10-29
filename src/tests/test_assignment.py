import datetime
from unittest import TestCase
from src.domain.assignment import Assignment
from src.repository.repo_assign import AssignmentRepository


class TestAssignment(TestCase):
    def setUp(self):
        self.__asg = Assignment("A3", "Lab Work", datetime.date(2023, 12, 12))
        self.__assignments = AssignmentRepository()

    def test_asg_1(self):
        test_asg = Assignment("A4", "Lab work", datetime.date.today())
        self.assertNotEqual(self.__asg, test_asg)

    def test_asg_2(self):
        self.__asg.id = "A8"
        self.assertEqual(self.__asg.id, "A8")

    def test_asg_3(self):
        self.__asg.desc = "SEMINAR"
        self.assertEqual(self.__asg.desc, "SEMINAR")

    def test_asg_4(self):
        self.__asg.deadline = datetime.date(2023, 8, 18)
        self.assertEqual(self.__asg.deadline, datetime.date(2023, 8, 18))

    def test_asg_5(self):
        self.assertNotEqual(self.__asg, "Assignment")

    def test_asg_6(self):
        string = "ID: A3, Description: Lab Work, Deadline: 2023-12-12"
        self.assertEqual(str(self.__asg), string)

    def test_stud_7(self):
        self.__assignments.add_assignment(self.__asg)
        list_assignments = self.__assignments.list_assignments()
        self.assertIn(self.__asg, list_assignments)

    def test_stud_8(self):
        self.__assignments.add_assignment(self.__asg)
        self.__assignments.add_assignment(Assignment("A2", "SEMINAR", datetime.date.today()))
        self.__assignments.add_assignment(Assignment("A4", "LAB", datetime.date.today()))
        self.__assignments.remove_assignment("A2")
        list_assignments = self.__assignments.list_assignments()
        self.assertNotIn(Assignment("A2", "SEMINAR", datetime.date.today()), list_assignments)

    def test_stud_9(self):
        self.__assignments.add_assignment(self.__asg)
        self.__assignments.add_assignment(Assignment("A2", "SEMINAR", datetime.date.today()))
        self.__assignments.add_assignment(Assignment("A4", "LAB", datetime.date.today()))
        self.__assignments.update_assignment("A4", "LAB", datetime.date.today())
        list_assignments = self.__assignments.list_assignments()
        self.assertNotIn(Assignment("A4", "LAB", datetime.date.today()), list_assignments)
