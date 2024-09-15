import os
import logging

from django.core.files.storage import default_storage

from .models import Student


logger = logging.getLogger(__name__)


def handle_file_upload(file):
    """
    Utility function to handle saving a file to the default storage system in the 'uploads' folder.

    Args:
        file: The uploaded file instance.

    Returns:
        str: The file path where the file is stored.
    """

    upload_folder = 'uploads/'


    file_name = file.name
    file_path = os.path.join(upload_folder, file_name)

    file_path = default_storage.save(file_path, file)

    return file_path


def create_student(name, student_id, department, email):
    """
    Utility function to handle the creation of a student record.

    Args:
        name (str): The student's name.
        student_id (str): The student's ID.
        department (str): The student's department.
        email (str): The student's email.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:

        if Student.objects.filter(student_id=student_id).exists():
            logger.error(f"Student with ID {student_id} already exists")
            return f"Student with ID {student_id} already exists."

        if Student.objects.filter(email=email).exists():
            logger.error(f"Student with email {email} already exists")
            return f"Student with email {email} already exists."


        Student.objects.create(
            name=name,
            student_id=student_id,
            department=department,
            email=email
        )
        logger.info(f"Student with ID {student_id} created")
        return f"Student with ID {student_id} created successfully."

    except Exception as e:
        logger.error(f"Error creating student: {e}")
        return f"Error creating student: {e}"
