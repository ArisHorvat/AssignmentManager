import datetime
from src.domain.grade import Grade
from src.repository.repo_exception import RepositoryException


class GradeIterator:
    def __init__(self, entity):
        self.__entity = entity
        self.__pos = -1

    def __next__(self):
        self.__pos += 1
        if self.__pos == len(self.__entity):
            raise StopIteration()
        return self.__entity[self.__pos]


class GradeRepository:
    def __init__(self, undo_service):
        self.__grades = []
        self.__undo = undo_service

    def __iter__(self):
        return GradeIterator(self.__grades)

    def list_grade(self):
        """
        This functions returns a list of all the grades
        :return:
        """
        return self.__grades

    def add_grade(self, grade: Grade):
        """
        This functions adds a grade to the repository
        :param grade:
        :return:
        """
        self.__grades.append(grade)

    def remove_grade_student(self, stud_id):
        """
        This function removes a grade from the repository after
            a student was removed from the database
        :param stud_id:
        :return:
        """
        indexes = []
        operations = []
        for i in range(len(self.__grades)):
            grade = self.__grades[i]
            if grade.stud_id == stud_id:
                indexes.append(i)
                operations.append(grade)
        for i in range(len(indexes)):
            index = indexes[i] - i
            self.__grades.pop(index)
        return operations

    def remove_grade_assignment(self, asg_id):
        """
        This function removes a grade from the repository after
            an assignment was removed
        :param asg_id:
        :return:
        """
        indexes = []
        operations = []
        for i in range(len(self.__grades)):
            grade = self.__grades[i]
            if grade.asg_id == asg_id:
                indexes.append(i)
                operations.append(grade)
        for i in range(len(indexes)):
            index = indexes[i] - i
            self.__grades.pop(index)
        return operations

    def give_student(self, asg_id: str, stud_id: int):
        """
        This function gives an assignment to one student
        :param asg_id:
        :param stud_id:
        :return:
        """
        for i in self.__grades:
            if i.stud_id == stud_id and i.asg_id == asg_id:
                raise RepositoryException("The student %s has the assignment %s" % (str(stud_id), asg_id))
        grade = Grade(asg_id, stud_id, 0)
        self.__grades.append(grade)

    def give_group(self, asg_id: str, group: int, students: list):
        """
        This function gives an assignment to a group
        :param asg_id:
        :param group:
        :param students:
        :return:
        """
        for i in students:
            verif = 0
            if i.group == group:

                for j in self.__grades:
                    if j.stud_id == i.id and j.asg_id == asg_id:
                        verif = 1

                if verif == 0:
                    grade = Grade(asg_id, i.id, 0)
                    self.__grades.append(grade)

    def ungraded(self, stud_id: int):
        """
        This function return a list of all ungraded assignments of a student
        :param stud_id:
        :return:
        """
        list_ungraded = []
        for i in self.__grades:
            if i.stud_id == stud_id and i.value == 0:
                list_ungraded.append(i.asg_id)
        if len(list_ungraded) == 0:
            raise RepositoryException("There aren't any ungraded assignments")
        return list_ungraded

    def grade_asg(self, asg_id: str, stud_id: int, value: int):
        """
        This function grades an assignment
        :param asg_id:
        :param stud_id:
        :param value:
        :return:
        """
        if value < 1 or value > 10:
            raise RepositoryException("Grade has to be between 1 - 10")
        final_grade = Grade(asg_id, stud_id, value)
        for i in range(len(self.__grades)):
            grade = self.__grades[i]
            if final_grade == grade:
                if grade.value == 0:
                    self.__grades[i] = final_grade
                else:
                    raise RepositoryException("You can't change the grade of an assignment")

    def ungrade_student(self, asg_id: str, stud_id: int, value: int):
        final_grade = Grade(asg_id, stud_id, value)
        indexes = []
        for i in range(len(self.__grades)):
            grade = self.__grades[i]
            if final_grade == grade:
                indexes.append(i)
        for i in range(len(indexes)):
            index = indexes[i] - i
            self.__grades.pop(index)

    def ungrade_students(self, asg_id: str, group: int, students: list):
        indexes = []

        for i in students:
            if i.group == group:
                for j in range(len(self.__grades)):
                    grade = self.__grades[j]
                    if grade.stud_id == i.id and grade.asg_id == asg_id:
                        indexes.append(j)

        for i in range(len(indexes)):
            index = indexes[i] - i
            self.__grades.pop(index)

    def order_grade(self, asg_id: str):
        """
        This function returns a list of the students and grades,
            in descending order of a given assignment
        :param asg_id:
        :return:
        """
        list_grades = []
        for i in self.__grades:
            if i.asg_id == asg_id:
                list_grades.append(i)

        for i in range(len(list_grades) - 1):
            for j in range(i + 1, len(list_grades)):
                grade1 = list_grades[i]
                grade2 = list_grades[j]
                if grade1.value < grade2.value:
                    aux = list_grades[i]
                    list_grades[i] = list_grades[j]
                    list_grades[j] = aux

        return list_grades

    def late_grade(self, students, assignments):
        """
        This functions returns a list of all the students who are late in
            handing an assignment
        :param students:
        :param assignments:
        :return:
        """
        list_ungraded = []
        for i in self.__grades:
            if i.value == 0:
                list_ungraded.append(i)

        list_deadline = []
        for i in assignments:
            for j in list_ungraded:
                str_dl = str(i.deadline)
                year = int(str_dl[0:4])
                month = int(str_dl[5:7])
                day = int(str_dl[9:])
                dl = datetime.datetime(year, month, day)
                today = datetime.datetime.now()
                if i.id == j.asg_id and dl < today:
                    list_deadline.append(j.stud_id)

        list_students = []
        for i in students:
            for j in list_deadline:
                if i.id == j:
                    list_students.append(i)
        return list_students

    def best_grade(self, students):
        """
        This function returns a list of all the students, in descending order,
            ordered by their school situations
        :param students:
        :return:
        """
        grades = {}
        assignments = {}
        averages = []

        for i in students:
            grades[i.id] = 0
            assignments[i.id] = 0

        for i in students:
            for j in self.__grades:
                if j.value != 0 and j.stud_id == i.id:
                    grades[i.id] += j.value
                    assignments[i.id] += 1

        for i in students:
            average = 0
            if assignments[i.id] != 0:
                average = grades[i.id] / assignments[i.id]
            if average != 0:
                averages.append([i, average])

        for i in range(len(averages) - 1):
            for j in range(i + 1, len(averages)):
                grade1 = averages[i][1]
                grade2 = averages[j][1]
                if grade1 < grade2:
                    averages[i], averages[j] = averages[j], averages[i]

        return averages
