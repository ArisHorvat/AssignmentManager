from unittest import TestCase
from src.domain.grade import Grade
from src.repository.repo_grade import GradeRepository


class TestGrade(TestCase):
    def setUp(self):
        self.__grade = Grade("A3", 8, 8)
        self.__grades = GradeRepository()

    def test_grade_1(self):
        test_grade = Grade("A3", 8, 8)
        self.assertEqual(self.__grade, test_grade)

    def test_grade_2(self):
        self.__grade.asg_id = "A14"
        self.assertEqual(self.__grade.asg_id, "A14")

    def test_grade_3(self):
        self.__grade.stud_id = 104
        self.assertEqual(self.__grade.stud_id, 104)

    def test_grade_4(self):
        self.__grade.value = 10
        self.assertEqual(self.__grade.value, 10)

    def test_grade_5(self):
        self.assertNotEqual(self.__grade, "Teacher")

    def test_grade_6(self):
        string = "Assignment: A3, Student: 8, Grade: 8"
        self.assertEqual(str(self.__grade), string)
