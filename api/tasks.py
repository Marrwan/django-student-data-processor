# tasks.py
from zipfile import BadZipFile

from celery import shared_task
import pandas as pd
import logging

from core.celery import app
from .utils import create_student
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@app.task
def process_file(file_path):
    try:
        logger.info(f"Processing file {file_path}")
        data = None
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path, header=0)
        elif file_path.endswith('.xlsx'):
            try:
                # Specify engine explicitly, for example, openpyxl for .xlsx files
                data = pd.read_excel(file_path, engine='openpyxl')
            except BadZipFile:
                error_message = f"Error processing file: File is not a valid Excel file (zip format issue)"
                logger.error(error_message)
                return {'error': error_message}
            except ValueError as e:
                error_message = f"Error processing file: {e}"
                logger.error(error_message)
                return {'error': error_message}
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, engine='xlrd')

        data.columns = data.columns.str.strip()

        required_columns = ['name', 'student_id', 'department', 'email']
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            error_message = f"Missing columns: {missing_columns}"
            logger.error(error_message)
            # self.update_state(state='FAILURE', meta={'error': error_message})
            return {'error': error_message}

        error_messages = []
        success_messages = []

        for index, row in data.iterrows():
            result = create_student(
                name=row['name'],
                student_id=row['student_id'],
                department=row['department'],
                email=row['email']
            )
            if "Error" in result:
                error_messages.append(result)
            else:
                success_messages.append(result)

        logger.info("File processed successfully")
        send_admin_notification()


        return {
            'status': 'File processed successfully',
            'success': success_messages,
            'errors': error_messages
        }

    except Exception as e:
        error_message = f"Error processing file: {e}"
        logger.error(error_message)
        # self.update_state(state='FAILURE', meta={'error': error_message})
        return {'error': error_message}

def send_admin_notification():
    subject = "Student Data Upload Completed"
    message = "The student data file has been successfully processed and uploaded."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['admin@admin.com']
    send_mail(subject, message, email_from, recipient_list)
