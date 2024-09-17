from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend

from .models import Student
from .serializer import StudentSerializer, FileUploadSerializer
from .tasks import process_file
from rest_framework import status

from .utils import handle_file_upload


class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data['file']
            file_path = handle_file_upload(file)


            # process_file(file_path)
            process_file.delay(file_path)

            return Response({"message": "File uploaded successfully, processing in the background"},
                            status=status.HTTP_202_ACCEPTED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StudentFilter(FilterSet):
    department = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['department']

class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']
    filterset_class = StudentFilter

