import datetime


class Assignment:
    def __init__(self, id: str, desc: str, deadline: datetime):
        self.__id = id
        self.__desc = desc
        self.__deadline = deadline

    @property
    def id(self):
        return self.__id

    @property
    def desc(self):
        return self.__desc

    @property
    def deadline(self):
        return self.__deadline

    @id.setter
    def id(self, id):
        self.__id = id

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @deadline.setter
    def deadline(self, deadline):
        self.__deadline = deadline

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return False
        return self.__id == other.id and self.__desc == other.desc and self.__deadline == other.deadline

    def __str__(self):
        return "ID: " + self.__id + ", Description: " + self.__desc + ", Deadline: " + str(self.__deadline)

