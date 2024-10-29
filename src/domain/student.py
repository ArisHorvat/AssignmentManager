class Student:
    def __init__(self, id: int, name: str, group: int):
        self.__id = id
        self.__name = name
        self.__group = group

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def group(self):
        return self.__group

    @id.setter
    def id(self, id):
        self.__id = id

    @name.setter
    def name(self, name):
        self.__name = name

    @group.setter
    def group(self, group):
        self.__group = group

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.__id == other.id and self.__name == other.name and self.__group == other.group

    def __str__(self):
        return "ID: " + str(self.__id) + ", Name: " + self.__name + ", Group: " + str(self.__group)
