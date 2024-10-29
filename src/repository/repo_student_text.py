from src.domain.student import Student
from src.repository.repo_student import StudentRepository


class StudentRepoText(StudentRepository):
    def __init__(self, file_name="student.txt"):
        super(StudentRepoText, self).__init__()
        self.__file_name = file_name
        self.load_file()

    def load_file(self):
        file = open(self.__file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            current = line.split(';')
            student = Student(int(current[0].strip()), current[1].strip(), int(current[2].strip()))
            super().add_student(student)

    def save_file(self):
        file = open(self.__file_name, 'wt')
        for student in self.list_students():
            output = str(student.id) + ";" + str(student.name) + ";" + str(student.group) + "\n"
            file.write(output)
        file.close()

    def add_student(self, student: Student):
        super(StudentRepoText, self).add_student(student)
        self.save_file()

    def remove_student(self, stud_id: int):
        old_args = super(StudentRepoText, self).remove_student(stud_id)
        self.save_file()
        return old_args

    def update_student(self, stud_id: int, name: str, group: int):
        old_args = super(StudentRepoText, self).update_student(stud_id, name, group)
        self.save_file()
        return old_args
