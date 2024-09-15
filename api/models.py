from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

