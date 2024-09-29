# your_app/utils.py

from django.core.exceptions import PermissionDenied

def department_required(function):
    def wrap(request, *args, **kwargs):
        if not getattr(request.user, 'is_department', False):
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap
from django.core.exceptions import PermissionDenied

def admin_required(user):
    if user.is_staff or user.is_superuser:
        return True
    raise PermissionDenied

def send_prize_notification_emails(winners, event):
    # Implement the email sending logic here
    pass


