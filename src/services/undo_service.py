class UndoException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return str(self.__msg)


class FunctionCall:
    def __init__(self, function_name, *function_args):
        self.__function = function_name
        self.__arguments = function_args

    def __call__(self, *args, **kwargs):
        self.__function(*self.__arguments)

    def __str__(self):
        my_string = str(self.__function.__name__) + "("
        for arg in self.__arguments:
            my_string += str(arg) + ","
        my_string += ")"
        return my_string


class Operation:
    def __init__(self, function_undo, function_redo):
        self.__function_undo = function_undo
        self.__function_redo = function_redo

    def undo(self):
        self.__function_undo()

    def redo(self):
        self.__function_redo()

    def __str__(self):
        my_string = ""
        my_string += "Undo: " + str(self.__function_undo) + "\n"
        my_string += "Redo: " + str(self.__function_redo) + "\n"
        return my_string


class CascadeOperation:
    def __init__(self, *operations):
        self.__operations = operations

    def undo(self):
        for operation in self.__operations:
            operation.undo()

    def redo(self):
        for operation in self.__operations:
            operation.redo()

    def __str__(self):
        my_string = "Cascade Operation:\n"
        for operation in self.__operations:
            my_string += str(operation)
        return my_string


class UndoService:
    def __init__(self):
        self.__history = []
        self.__index = -1

    def record(self, operation):
        self.__history = self.__history[0:self.__index+1][:]
        self.__history.append(operation)
        self.__index += 1

    def undo(self):
        if self.__index == -1:
            raise UndoException("There are no operations to undo")

        operation = self.__history[self.__index]
        operation.undo()
        self.__index -= 1

    def redo(self):
        if self.__index + 1 == len(self.__history):
            raise UndoException("There are no operations to redo")

        self.__index += 1
        operation = self.__history[self.__index]
        operation.redo()

    @staticmethod
    def new_add_operation(remove_call, remove_args, add_call, add_args):
        undo_function = FunctionCall(remove_call, *remove_args)
        redo_function = FunctionCall(add_call, *add_args)
        return Operation(undo_function, redo_function)

    @staticmethod
    def new_remove_operation(remove_call, remove_args, add_call, add_args):
        undo_function = FunctionCall(add_call, *add_args)
        redo_function = FunctionCall(remove_call, *remove_args)
        return Operation(undo_function, redo_function)

    @staticmethod
    def new_update_operation(function, old_args, new_args):
        undo_function = FunctionCall(function, *old_args)
        redo_function = FunctionCall(function, *new_args)
        return Operation(undo_function, redo_function)

    @staticmethod
    def transform_into_cascading_operation(*operations):
        return CascadeOperation(*operations)

    def new_cascade_operation(self, *operations):
        self.record(self.transform_into_cascading_operation(*operations))

    def __str__(self):
        my_string = "History:\n"
        for op in self.__history:
            my_string += str(op) + "\n"
        return my_string
