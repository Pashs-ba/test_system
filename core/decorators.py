from django.contrib import messages
from django.shortcuts import render, redirect


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_teacher):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Only admins can access this page')
        return redirect('homepage.html')
    return wrapper

