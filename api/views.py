from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from core.utils import upload_file
import zipfile
import platform
import os


@api_view(['POST'])
def create_test(request, pk):
    upload_file(request.FILES['tests'], f'contests/{pk}/tests/{pk}.zip')
    # upload_file(request.FILES['checker'], f'contest/{pk}') Need?
    upload_file(request.FILES['ideal_answer'], f'contests/{pk}.cpp')
    with zipfile.ZipFile(f'contests/{pk}/tests', 'r') as zip_f:
        zip_f.extractall(f'contests/{pk}/tests')
    return Response(status=HTTP_200_OK)



