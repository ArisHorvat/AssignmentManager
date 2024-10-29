import datetime
from src.domain.assignment import Assignment
from src.repository.repo_exception import RepositoryException


class AssignmentIterator:
    def __init__(self, entity):
        self.__entity = entity
        self.__pos = -1

    def __next__(self):
        self.__pos += 1
        if self.__pos == len(self.__entity):
            raise StopIteration()
        return self.__entity[self.__pos]


class AssignmentRepository:
    def __init__(self):
        self.__assignments = {}

    def __iter__(self):
        return AssignmentIterator(list(self.__assignments.values()))

    def add_assignment(self, asg: Assignment):
        """
        This function adds to the assignment repository an assignment
        :param asg:
        :return:
        """
        if asg.id in self.__assignments:
            raise RepositoryException("There exists an assignment with this ID")
        self.__assignments[asg.id] = asg

    def remove_assignment(self, asg_id: str):
        """
        This function removes an assignment from the repository
        :param asg_id:
        :return:
        """
        if asg_id not in self.__assignments:
            raise RepositoryException("There isn't an assignment with this ID")
        old_asg = self.__assignments[asg_id]
        old_args = [old_asg.id, old_asg.desc, old_asg.deadline]
        del self.__assignments[asg_id]
        return old_args

    def update_assignment(self, asg_id: str, desc: str, deadline: datetime):
        """
        This function updates an assignment from the repository from a given
            assignment id
        :param asg_id:
        :param desc:
        :param deadline:
        :return:
        """
        if asg_id not in self.__assignments:
            raise RepositoryException("There isn't an assignment with this ID")
        old_asg = self.__assignments[asg_id]
        old_args = [old_asg.id, old_asg.desc, old_asg.deadline]
        asg = Assignment(asg_id, desc, deadline)
        self.__assignments[asg_id] = asg
        return old_args

    def list_assignments(self):
        """
        This function returns a list containing all the assignments
        :return:
        """
        return list(self.__assignments.values())
