from src.domain.grade import Grade
from src.repository.repo_grade import GradeRepository


class GradeRepoText(GradeRepository):
    def __init__(self, undo_service):
        super(GradeRepoText, self).__init__(undo_service)
        self.__filename = "grade.txt"
        self.loadfile()

    def loadfile(self):
        file = open(self.__filename, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            current = line.split(";")
            grade = Grade(current[0].strip(), int(current[1].strip()), int(current[2].strip()))
            super().add_grade(grade)

    def savefile(self):
        file = open(self.__filename, 'wt')

        for grade in self.list_grade():
            output = grade.asg_id + ";" + str(grade.stud_id) + ";" + str(grade.value) + "\n"
            file.write(output)

        file.close()

    def add_grade(self, grade: Grade):
        super(GradeRepoText, self).add_grade(grade)
        self.savefile()

    def remove_grade_student(self, stud_id):
        operations = super(GradeRepoText, self).remove_grade_student(stud_id)
        self.savefile()
        return operations

    def remove_grade_assignment(self, asg_id):
        operations = super(GradeRepoText, self).remove_grade_assignment(asg_id)
        self.savefile()
        return operations

    def give_student(self, asg_id: str, stud_id: int):
        super(GradeRepoText, self).give_student(asg_id, stud_id)
        self.savefile()

    def give_group(self, asg_id: str, group: int, students: list):
        super(GradeRepoText, self).give_group(asg_id, group, students)
        self.savefile()

    def ungraded(self, stud_id: int):
        final_list = super(GradeRepoText, self).ungraded(stud_id)
        self.savefile()
        return final_list

    def grade_asg(self, asg_id: str, stud_id: int, value: int):
        super(GradeRepoText, self).grade_asg(asg_id, stud_id, value)
        self.savefile()

    def ungrade_student(self, asg_id: str, stud_id: int, value: int):
        super().ungrade_student(asg_id, stud_id, value)
        self.savefile()

    def ungrade_students(self, asg_id: str, group: int, students: list):
        super().ungrade_students(asg_id, group, students)
        self.savefile()

    def order_grade(self, asg_id: str):
        final_list = super(GradeRepoText, self).order_grade(asg_id)
        self.savefile()
        return final_list

    def late_grade(self, students, assignments):
        final_list = super(GradeRepoText, self).late_grade(students, assignments)
        self.savefile()
        return final_list

    def best_grade(self, students):
        final_list = super(GradeRepoText, self).best_grade(students)
        self.savefile()
        return final_list
