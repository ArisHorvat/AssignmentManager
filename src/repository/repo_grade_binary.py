import pickle

from src.domain.grade import Grade
from src.repository.repo_grade import GradeRepository


class GradeRepoBinary(GradeRepository):
    def __init__(self, undo_service):
        super(GradeRepoBinary, self).__init__(undo_service)
        self.__filename = 'grade.pickle'
        self.load_file()

    def load_file(self):
        try:
            file = open(self.__filename, 'rb')
            grades = pickle.load(file)

            for grade in grades:
                super().add_grade(grade)
            file.close()
        except EOFError as eoe:
            print(eoe)

    def write_file(self):
        file = open(self.__filename, "wb")
        pickle.dump(super().list_grade(), file)
        file.close()

    def add_grade(self, grade: Grade):
        super().add_grade(grade)
        self.write_file()

    def remove_grade_student(self, stud_id):
        operations = super().remove_grade_student(stud_id)
        self.write_file()
        return operations

    def remove_grade_assignment(self, asg_id):
        operations = super().remove_grade_assignment(asg_id)
        self.write_file()
        return operations

    def give_student(self, asg_id: str, stud_id: int):
        super().give_student(asg_id, stud_id)
        self.write_file()

    def give_group(self, asg_id: str, group: int, students: list):
        super().give_group(asg_id, group, students)
        self.write_file()

    def ungraded(self, stud_id: int):
        final_list = super().ungraded(stud_id)
        self.write_file()
        return final_list

    def grade_asg(self, asg_id: str, stud_id: int, value: int):
        super().grade_asg(asg_id, stud_id, value)
        self.write_file()

    def ungrade_student(self, asg_id: str, stud_id: int, value: int):
        super().ungrade_student(asg_id, stud_id, value)
        self.write_file()

    def ungrade_students(self, asg_id: str, group: int, students: list):
        super().ungrade_students(asg_id, group, students)
        self.write_file()

    def order_grade(self, asg_id: str):
        final_list = super().order_grade(asg_id)
        self.write_file()
        return final_list

    def late_grade(self, students, assignments):
        final_list = super().late_grade(students, assignments)
        self.write_file()
        return final_list

    def best_grade(self, students):
        final_list = super().best_grade(students)
        self.write_file()
        return final_list
