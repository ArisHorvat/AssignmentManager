import pickle
from datetime import datetime

from src.domain.assignment import Assignment
from src.repository.repo_assign import AssignmentRepository


class AssignmentRepoBinary(AssignmentRepository):
    def __init__(self, filename='assignment.pickle'):
        super(AssignmentRepoBinary, self).__init__()
        self.__filename = filename
        self.load_file()

    def load_file(self):
        try:
            file = open(self.__filename, 'rb')
            assignments = pickle.load(file)

            for asg in assignments:
                super().add_assignment(asg)

            file.close()
        except EOFError as eoe:
            pass

    def write_file(self):
        file = open(self.__filename, 'wb')
        pickle.dump(self.list_assignments(), file)
        file.close()

    def add_assignment(self, asg: Assignment):
        super().add_assignment(asg)
        self.write_file()

    def remove_assignment(self, asg_id: str):
        old_args = super().remove_assignment(asg_id)
        self.write_file()
        return old_args

    def update_assignment(self, asg_id: str, desc: str, deadline: datetime):
        old_args = super().update_assignment(asg_id, desc, deadline)
        self.write_file()
        return old_args
