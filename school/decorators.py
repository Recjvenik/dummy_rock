from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def teacher_required(view_func):
    """Allow access only to users with role 'teacher' or 'school_admin' or 'admin'."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.path)
        if request.user.role not in ('teacher', 'school_admin', 'admin'):
            messages.error(request, 'This page is for teachers only.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


def school_admin_required(view_func):
    """Allow access only to users with role 'school_admin' or 'admin'."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.path)
        if request.user.role not in ('school_admin', 'admin'):
            messages.error(request, 'This page is for school administrators only.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper
