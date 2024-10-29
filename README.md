# 💻Assignment Manager

**Assignment Manager** is a Python-based application designed to help manage students and assignments efficiently. Using a layered architecture, the application allows for CRUD operations on students and assignments, as well as features like grading, ordering, and filtering of data. The system also supports undo/redo operations and provides options for various data storage methods, including in-memory, text files, and binary files.

## Features

- **Student and Assignment Management**
  - Add, update, remove, and list students or assignments.
  - Assign assignments to individual students or groups.
  - Grade students on their assignments.
- **Sorting and Filtering**
  - Order students by their grades on a specific assignment.
  - Show students who are late in submitting assignments.
  - Sort students based on their average grade across assignments.
- **Undo/Redo Operations**
  - Support for undo and redo actions across multiple operations.

## Architecture

The application uses a layered architecture, organized into several key layers:

1. **User Interface (UI)**:
   - A simple interface that provides options to manage students and assignments, grade students, and view sorted or filtered information.
  
2. **Services Layer**:
   - This layer handles all business logic, such as CRUD operations, filtering, and sorting functionalities.
   - Includes an `UndoService` for managing undo and redo operations.

3. **Repository Layer**:
   - **Student Repository** (`repo_students`)
   - **Assignment Repository** (`repo_assignments`)
   - **Grade Repository** (`repo_grades`)
   - **Exception Repository** (`repo_exceptions`) for handling custom exceptions.

   Each repository can be configured to store data in:
   - **In-Memory**: Stores data temporarily during runtime.
   - **Text File**: Reads and writes data to a text file.
   - **Binary File**: Uses `pickle` to read and write data in a binary format for more efficient storage.

4. **Domain Layer**:
   - Contains data models, including classes for:
     - `Student`
     - `Assignment`
     - `Grade`
   - Each class represents a distinct entity within the system with its respective attributes and methods.

5. **Testing**:
   - Unit tests are included for each class to ensure the functionality and reliability of the system.
