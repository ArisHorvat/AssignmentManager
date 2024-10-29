from datetime import datetime

from src.domain.assignment import Assignment
from src.repository.repo_assign import AssignmentRepository


class AssignmentRepoText(AssignmentRepository):
    def __init__(self, filename='assignment.txt'):
        super(AssignmentRepoText, self).__init__()
        self.__filename = filename
        self.load_file()

    def load_file(self):
        file = open(self.__filename, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            current = line.split(";")
            asg = Assignment(current[0].strip(), current[1].strip(), datetime.strptime(current[2].strip(), "%Y-%m-%d"))
            super().add_assignment(asg)

    def save_file(self):
        file = open(self.__filename, 'wt')
        for asg in self.list_assignments():
            output = str(asg.id) + ";" + str(asg.desc) + ";" + str(asg.deadline) + "\n"
            file.write(output)
        file.close()

    def add_assignment(self, asg: Assignment):
        super(AssignmentRepoText, self).add_assignment(asg)
        self.save_file()

    def remove_assignment(self, asg_id: str):
        old_args = super(AssignmentRepoText, self).remove_assignment(asg_id)
        self.save_file()
        return old_args

    def update_assignment(self, asg_id: str, desc: str, deadline: datetime):
        old_args = super(AssignmentRepoText, self).update_assignment(asg_id, desc, deadline)
        self.save_file()
        return old_args
