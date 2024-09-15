import pytest
from api.serializer import FileUploadSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_valid_file_upload():
    valid_file = SimpleUploadedFile("students.csv", b"name,student_id,department,email\nJohn,12345,CS,john@example.com")
    serializer = FileUploadSerializer(data={'file': valid_file})
    assert serializer.is_valid()

@pytest.mark.django_db
def test_invalid_file_upload():
    invalid_file = SimpleUploadedFile("students.txt", b"Invalid content")
    serializer = FileUploadSerializer(data={'file': invalid_file})
    assert not serializer.is_valid()
    assert "Unsupported file type" in str(serializer.errors['file'][0])
