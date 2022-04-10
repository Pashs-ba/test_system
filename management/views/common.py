from django.shortcuts import render, redirect
from core.decorators import admin_only
from ..utils import create_user, add_tests, create_ans, upload_tests, generate_variants_question, create_name, create_password
from core.models import *
from django.db import transaction
from django.contrib import messages
from ..forms import CompetitionForm, ContestCreationForm, ContestUpdateForm, QuestionCreationForm, GroupForm, QuestionGeneratorForm, MikeForm, TeacherCompetitionForm, TeacherGroupForm
from django.conf import settings
import os.path
import shutil
from threading import Thread
from django.core.paginator import Paginator
from django.http import HttpResponse
import ast
import json
from django.db.models import Count
from core.utils import upload_file
from zipfile import ZipFile
from django.contrib.auth import authenticate


@admin_only
def management_page(request):
    return render(request, 'management.html')

