from unittest import TestCase
from src.domain.student import Student
from src.repository.repo_student import StudentRepository

class TestStudent(TestCase):
    def setUp(self):
        self.__stud = Student(8, "Chris", 404)
        self.__students = StudentRepository()

    def test_stud_1(self):
        test_student = Student(8, "Chris", 404)
        self.assertEqual(self.__stud, test_student)

    def test_stud_2(self):
        self.__stud.id = 10
        self.assertEqual(self.__stud.id, 10)

    def test_stud_3(self):
        self.__stud.name = "John"
        self.assertEqual(self.__stud.name, "John")

    def test_stud_4(self):
        self.__stud.group = 914
        self.assertEqual(self.__stud.group, 914)

    def test_stud_5(self):
        self.assertNotEqual(self.__stud, 8)

    def test_stud_6(self):
        string = "ID: 8, Name: Chris, Group: 404"
        self.assertEqual(str(self.__stud), string)

    def test_stud_7(self):
        self.__students.add_student(self.__stud)
        list_students = self.__students.list_students()
        self.assertIn(self.__stud, list_students)

    def test_stud_8(self):
        self.__students.add_student(self.__stud)
        self.__students.add_student(Student(103, "Marian", 913))
        self.__students.add_student(Student(110, "Mircea", 914))
        self.__students.remove_student(103)
        list_students = self.__students.list_students()
        self.assertNotIn(Student(103, "Marian", 913), list_students)

    def test_stud_9(self):
        self.__students.add_student(self.__stud)
        self.__students.add_student(Student(103, "Marian", 913))
        self.__students.update_student(103, 115, "Michael", 900)
        list_students = self.__students.list_students()
        self.assertNotIn(Student(103, "Marian", 913), list_students)
