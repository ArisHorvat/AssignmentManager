import datetime

from src.repository.repo_exception import RepositoryException
from src.services.services import Services
from src.services.undo_service import UndoService, UndoException


class UI:
    def __init__(self, student, assignment, grade, undo_service, value):
        self.__service = Services(student, assignment, grade, undo_service, value)
        self.__undo_service = undo_service

    def print_menu(self):
        print("")
        print("1. Manage students or assignments")
        print("2. Give assignments to a student or to a group")
        print("3. Grade a student")
        print("4. Order students by grade of an assignment")
        print("5. Show students who are late in handing an assignment")
        print("6. Students ordered by their average grade")
        print("7. Undo")
        print("8. Redo")
        print("9. Exit")

    def print_1(self):
        print("a. Students")
        print("b. Assignments")
        print("c. Exit")
        option = input("Option: ")
        return option

    def print_2(self):
        print("a. Give assignment to student")
        print("b. Give assignment to group")
        print("c. Exit")
        option = input("Option: ")
        return option

    def print_menu_manage(self, type: str):
        print("")
        print("1. Add " + type)
        print("2. Remove " + type)
        print("3. Update " + type)
        print("4. List " + type)
        print("5. Exit")

    def manage_students(self):
        while True:
            self.print_menu_manage("students")
            option = input("Choose one of the commands: ")
            if option == "1":
                try:
                    id = int(input("Choose an id: "))
                    name = input("Choose a name: ")
                    group = int(input("Choose a group: "))
                    self.__service.add_student(id, name, group)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "2":
                try:
                    id = int(input("Choose an id: "))
                    self.__service.remove_student(id)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "3":
                try:
                    stud_id = int(input("Choose the id of the student: "))
                    name = input("Change the name(optional): ")
                    group = int(input("Change the group(optional): "))
                    self.__service.update_student(stud_id, name, group)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "4":
                students = self.__service.list_student()
                for student in students:
                    print(student)
            elif option == "5":
                return
            else:
                print("Choose a valid command!")

    def manage_assignments(self):
        while True:
            self.print_menu_manage("assignments")
            option = input("Choose one of the commands: ")
            if option == "1":
                try:
                    asg_id = input("Choose an id: ")
                    desc = input("Choose a description: ")
                    year = int(input("Enter a year: "))
                    month = int(input("Enter a month: "))
                    day = int(input("Enter a day: "))
                    deadline = datetime.date(year, month, day)
                    self.__service.add_assignment(asg_id, desc, deadline)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "2":
                try:
                    id = input("Choose an id: ")
                    self.__service.remove_assignment(id)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "3":
                try:
                    asg_id = input("Choose the id of the assignment: ")
                    desc = input("Change the description(optional): ")
                    year = int(input("Change the year: "))
                    month = int(input("Change the month: "))
                    day = int(input("Change the day: "))
                    deadline = datetime.date(year, month, day)
                    self.__service.update_assignment(asg_id, desc, deadline)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "4":
                assignments = self.__service.list_assignment()
                for asg in assignments:
                    print(asg)
            elif option == "5":
                return
            else:
                print("Choose a valid command!")

    def print_ui(self):
        while True:
            self.print_menu()
            option = input("Choose one of the commands: ")
            if option == "1":
                while True:
                    command = self.print_1()
                    if command == "a":
                        self.manage_students()
                    elif command == "b":
                        self.manage_assignments()
                    elif command == "c":
                        break
                    else:
                        print("Invalid Command!")
            elif option == "2":
                while True:
                    command = self.print_2()
                    if command == "a":
                        try:
                            asg_id = input("Choose the id of the assignment: ")
                            stud_id = int(input("Choose the id of the student: "))
                            self.__service.give_student(asg_id, stud_id)
                            print("Command successful")
                        except ValueError as ve:
                            print(ve)
                        except RepositoryException as re:
                            print(re)
                    elif command == "b":
                        try:
                            asg_id = input("Choose the id of the assignment: ")
                            group = int(input("Choose the number of the group: "))
                            self.__service.give_group(asg_id, group)
                            print("Command successful")
                        except ValueError as ve:
                            print(ve)
                        except RepositoryException as re:
                            print(re)
                    elif command == "c":
                        break
                    else:
                        print("Invalid command!")
            elif option == "3":
                try:
                    stud_id = int(input("Choose the id of the student you want to grade: "))
                    list_ungraded = self.__service.ungraded(stud_id)
                    print("Here are the assignments where the student is not graded: ")
                    print(list_ungraded)
                    asg_id = input("Choose an assignment you want to grade: ")
                    grade = int(input("Choose the grade for this assignment: "))
                    self.__service.graded(asg_id, stud_id, grade)
                    print("Command successful")
                except ValueError as ve:
                    print(ve)
                except RepositoryException as re:
                    print(re)
            elif option == "4":
                try:
                    asg_id = input("Choose an assignment id: ")
                    final_list = self.__service.order_grade(asg_id)
                    print("Here is the list of the students that have assignment %s :" % asg_id)
                    for i in final_list:
                        print(i)
                except ValueError as ve:
                    print(ve)
            elif option == "5":
                print("Here is the list of students who are late in handing at least one assignment:")
                final_list = self.__service.late_grade()
                for i in final_list:
                    print(i)
            elif option == "6":
                print("Here is the list of students with the best school situation, ordered by average grade:")
                final_list = self.__service.best_grade()
                for i in final_list:
                    print(i[0], end=' ')
                    print("Average Grade: " + str(i[1]))
            elif option == "7":
                try:
                    self.__undo_service.undo()
                except UndoException as ue:
                    print(ue)
            elif option == "8":
                try:
                    self.__undo_service.redo()
                except UndoException as ue:
                    print(ue)
            elif option == "9":
                print("Bye!")
                return
            else:
                print("You didn't choose one of the commands! Try again")
