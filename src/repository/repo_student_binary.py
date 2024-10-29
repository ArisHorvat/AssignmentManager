import pickle

from src.domain.student import Student
from src.repository.repo_student import StudentRepository


class StudentRepoBinary(StudentRepository):
    def __init__(self, filename="student.pickle"):
        super(StudentRepoBinary, self).__init__()
        self.__filename = filename
        self.load_file()

    def write_file(self):
        file = open(self.__filename, 'wb')
        pickle.dump(self.list_students(), file)
        file.close()

    def load_file(self):
        try:
            file = open(self.__filename, 'rb')
            students_list = pickle.load(file)

            for student in students_list:
                super().add_student(student)

            file.close()
        except EOFError as eoe:
            print(eoe)

    def add_student(self, stud: Student):
        super().add_student(stud)
        self.write_file()

    def remove_student(self, stud_id: int):
        old_args = super().remove_student(stud_id)
        self.write_file()
        return old_args

    def update_student(self, stud_id: int, name: str, group: int):
        old_args = super().update_student(stud_id, name, group)
        self.write_file()
        return old_args
