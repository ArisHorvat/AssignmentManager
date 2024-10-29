from src.repository import repo_student, repo_assign, repo_grade, repo_student_text, repo_assign_text, repo_grade_text, \
    repo_student_binary, repo_assign_binary, repo_grade_binary
from src.repository.repo_assign import AssignmentRepository
from src.repository.repo_assign_binary import AssignmentRepoBinary
from src.repository.repo_assign_text import AssignmentRepoText
from src.repository.repo_grade import GradeRepository
from src.repository.repo_grade_binary import GradeRepoBinary
from src.repository.repo_grade_text import GradeRepoText
from src.repository.repo_student import StudentRepository
from src.repository.repo_student_binary import StudentRepoBinary
from src.repository.repo_student_text import StudentRepoText
from src.services.undo_service import UndoService
from src.ui.ui import UI
from jproperties import Properties


def get_prop():
    properties = Properties()

    with open('settings.properties', 'rb') as configuration_file:
        properties.load(configuration_file)
    repository_type = properties['repository'].data
    student_repo = properties['student'].data
    assignment_repo = properties['assignment'].data
    grade_repo = properties['grade'].data
    randomvalue = properties['random'].data

    return repository_type, student_repo, assignment_repo, grade_repo, randomvalue


if __name__ == "__main__":
    repo_type, repo1, repo2, repo3, value = get_prop()
    undo_service = UndoService()
    if repo_type == "in_memory":
        ui = UI(StudentRepository, AssignmentRepository,
                GradeRepository, undo_service, value)
    elif repo_type == "text":
        ui = UI(StudentRepoText, AssignmentRepoText,
                GradeRepoText, undo_service, value)
    elif repo_type == "binary":
        ui = UI(StudentRepoBinary, AssignmentRepoBinary,
                GradeRepoBinary, undo_service, value)
    else:
        print("There wasn't a valid type of file selected")
        exit(0)
    ui.print_ui()
