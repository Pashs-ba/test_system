from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from core.decorators import admin_only
from django.views.decorators.http import require_http_methods
from django.conf import settings
from core.models import Test
import os


@admin_only
@require_http_methods(["POST"])
def make_example(request):
    pk = request.POST['pk']
    test = Test.objects.get(pk=pk)
    test.is_example = not test.is_example
    test.save()
    return HttpResponse('OK')








