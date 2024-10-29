class Grade:
    def __init__(self, asg_id: str, stud_id: int, value: int):
        self.__asg_id = asg_id
        self.__stud_id = stud_id
        self.__value = value

    @property
    def asg_id(self):
        return self.__asg_id

    @property
    def stud_id(self):
        return self.__stud_id

    @property
    def value(self):
        return self.__value

    @asg_id.setter
    def asg_id(self, asg_id):
        self.__asg_id = asg_id

    @stud_id.setter
    def stud_id(self, stud_id):
        self.__stud_id = stud_id

    @value.setter
    def value(self, value):
        self.__value = value

    def __eq__(self, other):
        if not isinstance(other, Grade):
            return False
        return self.__asg_id == other.asg_id and self.__stud_id == other.stud_id

    def __str__(self):
        return "Assignment: " + self.__asg_id + ", Student: " + str(self.__stud_id) + ", Grade: " + str(self.__value)
