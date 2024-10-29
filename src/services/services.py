import datetime
import random

from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.student import Student
from src.repository.repo_exception import RepositoryException


class Services:
    def __init__(self, student, assignment, grade, undo_service, value):
        self.__repo_stud = student()
        self.__repo_asg = assignment()
        self.__repo_grade = grade(undo_service)
        self.__undo_service = undo_service
        if value == "True":
            self.generate_values()

    def generate_values(self):
        name = ["Andrei", "Eduard", "Mihai", "Mariana", "Veronica",
                "Andreea", "Victor", "Ariana", "Aris", "Cristian",
                "Cosmin", "Mara", "Patricia"]
        groups = ["100", "200", "300", "400", "500"]
        student_ids = []
        assignment_ids = []

        for i in range(20):
            stud_id = 100 + i
            stud_name = random.choice(name)
            group = int(random.choice(groups)) + random.randint(0, 5)
            student_ids.append(stud_id)
            self.add_student_random(stud_id, stud_name, group)

            as_id = "A" + str(i)
            desc = "Laboratory Work " + str(i)
            year = random.randint(2023, 2024)
            month = random.randint(1, 12)
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = random.randint(1, 31)
            elif month == 2:
                if year == 2024:
                    day = random.randint(1, 29)
                else:
                    day = random.randint(1, 28)
            else:
                day = random.randint(1, 30)
            deadline = datetime.date(year, month, day)
            assignment_ids.append(as_id)
            self.add_assignment_random(as_id, desc, deadline)

        for i in range(20):
            while True:
                verif = 0
                stud_id = random.choice(student_ids)
                asg_id = random.choice(assignment_ids)
                value = random.randint(0, 10)
                grade = Grade(asg_id, stud_id, value)
                grades = self.__repo_grade.list_grade()
                for i in grades:
                    if i == grade:
                        verif = 1
                if verif == 0:
                    break
            self.__repo_grade.add_grade(grade)

    def add_student(self, id: int, name: str, group: int):
        """
        This function sends the command to the student repo to add
            a student
        :param id:
        :param name:
        :param group:
        :return:
        """
        stud = Student(id, name, group)
        self.__repo_stud.add_student(stud)
        operation = self.__undo_service.new_add_operation(self.__repo_stud.remove_student,
                                                          [id], self.__repo_stud.add_student, [stud])
        self.__undo_service.record(operation)

    def add_student_random(self, id: int, name: str, group: int):
        """
        This function sends the command to the student repo to add
            a student
        :param id:
        :param name:
        :param group:
        :return:
        """
        stud = Student(id, name, group)
        self.__repo_stud.add_student(stud)

    def remove_student(self, id: int):
        """
        This function sends the command to the student repo to remove
            a student
        :param id:
        :return:
        """
        all_operations = ()

        old_args = self.__repo_stud.remove_student(id)
        stud = Student(old_args[0], old_args[1], old_args[2])
        student_operation = self.__undo_service.new_remove_operation(self.__repo_stud.remove_student, [id],
                                                                     self.__repo_stud.add_student, [stud])

        all_operations += (student_operation, )

        old_args = self.__repo_grade.remove_grade_student(id)
        for grades in old_args:
            grade_operation = self.__undo_service.new_remove_operation(self.__repo_grade.remove_grade_student, [id],
                                                                       self.__repo_grade.add_grade, [grades])
            all_operations += (grade_operation, )

        self.__undo_service.new_cascade_operation(*all_operations)

    def update_student(self, stud_id: int, name: str, group: int):
        """
        This function sends the command to the student repo to update
            the properties of a student
        :param stud_id:
        :param name:
        :param group:
        :return:
        """
        old_args = self.__repo_stud.update_student(stud_id, name, group)
        operation = self.__undo_service.new_update_operation(self.__repo_stud.update_student,
                                                                 old_args, [stud_id, name, group])
        self.__undo_service.record(operation)

    def list_student(self):
        """
        This function returns a list of all the students from the repository
        :return:
        """
        return self.__repo_stud.list_students()

    def add_assignment(self, id: str, desc: str, deadline: datetime):
        """
        This function sends the command to the repo to add an assignment
        :param id:
        :param desc:
        :param deadline:
        :return:
        """
        asg = Assignment(id, desc, deadline)
        self.__repo_asg.add_assignment(asg)
        operation = self.__undo_service.new_add_operation(self.__repo_asg.remove_assignment, [id],
                                                          self.__repo_asg.add_assignment, [asg])

        self.__undo_service.record(operation)

    def add_assignment_random(self, id: str, desc: str, deadline: datetime):
        """
        This function sends the command to the repo to add an assignment
        :param id:
        :param desc:
        :param deadline:
        :return:
        """
        asg = Assignment(id, desc, deadline)
        self.__repo_asg.add_assignment(asg)

    def remove_assignment(self, id: str):
        """
        This function sends the command to the repo to remove an
            assignment
        :param id:
        :return:
        """
        all_operations = ()

        old_args = self.__repo_asg.remove_assignment(id)
        asg = Assignment(old_args[0], old_args[1], old_args[2])
        asg_operation = self.__undo_service.new_remove_operation(self.__repo_asg.remove_assignment, [id],
                                                                 self.__repo_asg.add_assignment, [asg])

        all_operations += (asg_operation,)

        grades = self.__repo_grade.remove_grade_assignment(id)
        for grade in grades:
            grade_operation = self.__undo_service.new_remove_operation(self.__repo_grade.remove_grade_assignment,
                                                                       [id], self.__repo_grade.add_grade, [grade])
            all_operations += (grade_operation,)

        self.__undo_service.new_cascade_operation(*all_operations)

    def update_assignment(self, asg_id: str, desc: str, deadline: datetime):
        """
        This function sends a command to the repo to update one of the
            assignments
        :param asg_id:
        :param desc:
        :param deadline:
        :return:
        """
        old_args = self.__repo_asg.update_assignment(asg_id, desc, deadline)
        operation = self.__undo_service.new_update_operation(self.__repo_asg.update_assignment,
                                                             old_args, [asg_id, desc, deadline])
        self.__undo_service.record(operation)

    def list_assignment(self):
        """
        This function returns a list of all the assignments
        :return:
        """
        return self.__repo_asg.list_assignments()

    def give_student(self, asg_id: str, stud_id: int):
        """
        This function sends the command to the repository to give
            a student an assignment
        :param asg_id:
        :param stud_id:
        :return:
        """
        self.__repo_grade.give_student(asg_id, stud_id)
        operation = self.__undo_service.new_add_operation(self.__repo_grade.ungrade_student, [asg_id, stud_id, 0],
                                                          self.__repo_grade.give_student, [asg_id, stud_id])
        self.__undo_service.record(operation)

    def give_group(self, asg_id: str, group: int):
        """
        This function sends the command to the repository to give a group
            an assignment
        :param asg_id:
        :param group:
        :return:
        """
        students = self.__repo_stud.list_students()
        self.__repo_grade.give_group(asg_id, group, students)
        operation = self.__undo_service.new_add_operation(self.__repo_grade.ungrade_students,
                                                          [asg_id, group, students],
                                                          self.__repo_grade.give_student, [asg_id, group, students])
        self.__undo_service.record(operation)

    def ungraded(self, stud_id: int):
        """
        This function returns a list of all the ungraded assignments
            of a student
        :param stud_id:
        :return:
        """
        return self.__repo_grade.ungraded(stud_id)

    def graded(self, asg_id: str, stud_id: int, grade: int):
        """
        This function sends the command to the repository to grade
            an assignment of one student
        :param asg_id:
        :param stud_id:
        :param grade:
        :return:
        """
        self.__repo_grade.grade_asg(asg_id, stud_id, grade)
        operation = self.__undo_service.new_add_operation(self.__repo_grade.ungrade_student,
                                                          [asg_id, stud_id, grade],
                                                          self.__repo_grade.grade_asg, [asg_id, stud_id, grade])
        self.__undo_service.record(operation)

    def order_grade(self, asg_id: str):
        """
        This function returns a list of all students who had an assignment
            and ordered them descending by their grade
        :param asg_id:
        :return:
        """
        return self.__repo_grade.order_grade(asg_id)

    def late_grade(self):
        """
        This function returns all the students who are late in
            handing one assignment
        :return:
        """
        assignments = self.__repo_asg.list_assignments()
        students = self.__repo_stud.list_students()
        return self.__repo_grade.late_grade(students, assignments)

    def best_grade(self):
        """
        This function returns a list of all the students ordered by their
            school situation in descending order
        :return:
        """
        students = self.__repo_stud.list_students()
        return self.__repo_grade.best_grade(students)
