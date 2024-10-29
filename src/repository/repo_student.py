import datetime

from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.student import Student
from src.repository.repo_exception import RepositoryException


class StudentIterator:
    def __init__(self, entity):
        self.__entity = entity
        self.__pos = -1

    def __next__(self):
        self.__pos += 1
        if self.__pos == len(self.__entity):
            raise StopIteration()
        return self.__entity[self.__pos]


class StudentRepository:
    def __init__(self):
        self.__students = {}

    def __iter__(self):
        return StudentIterator(list(self.__students.values()))

    def add_student(self, stud: Student):
        """
        This functions adds a student to the repository
        :param stud:
        :return:
        """
        if stud.id in self.__students:
            raise RepositoryException("There exists a student with this ID!")
        self.__students[stud.id] = stud

    def remove_student(self, stud_id: int):
        """
        This function removes a student from the repository
        :param stud_id:
        :return:
        """
        if stud_id not in self.__students:
            raise RepositoryException("There isn't a student with this ID")
        old_stud = self.__students[stud_id]
        old_args = [old_stud.id, old_stud.name, old_stud.group]
        del self.__students[stud_id]
        return old_args

    def update_student(self, stud_id: int, name: str, group: int):
        """
        This function updates a student from the repository
        :param stud_id:
        :param name:
        :param group:
        :return:
        """
        if stud_id not in self.__students:
            raise RepositoryException("There isn't a student with this ID")
        old_stud = self.__students[stud_id]
        old_args = [old_stud.id, old_stud.name, old_stud.group]
        stud = Student(stud_id, name, group)
        self.__students[stud_id] = stud
        return old_args

    def list_students(self):
        """
        This function returns a list of all students
        :return:
        """
        return list(self.__students.values())
