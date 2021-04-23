from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user
from core.models import *
from django.db import transaction
from django.contrib import messages


@admin_only
def user_panel(request):
    context = {}
    context.update({'users': Passwords.objects.all()})
    return render(request, 'user_panel.html', context)


@admin_only
def management_page(request):
    return render(request, 'management.html')


@admin_only
def delete_user(request, pk):
    if request.method == "POST":
        print(pk)
        a = Users.objects.get(pk=pk)
        messages.info(request, f'Successful delete user {a.username}')
        a.delete()
        return redirect('user-management')
    else:
        return render(request, 'user_delete.html')


@transaction.atomic
@admin_only
def user_generating(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        if request.POST['num']:
            users = []
            for i in range(int(request.POST['num'])):
                users.append(create_user())
            context.update({'users': users})

            messages.info(request, f'Successful created {request.POST["num"]} users')
            return redirect('user-management')
    else:
        return render(request, 'user_generating.html')