from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'department', 'email']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):

        file_extension = value.name.split('.')[-1].lower()


        if file_extension not in ['csv', 'xlsx', 'xls']:
            raise serializers.ValidationError("Unsupported file type. Only CSV and Excel files are allowed.")


        return value
