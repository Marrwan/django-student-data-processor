from django.urls import path

from django.contrib import admin
from api.views import FileUploadView, StudentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('students/', StudentListView.as_view(), name='student-list'),

]
