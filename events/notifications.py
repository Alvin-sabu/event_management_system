# events/notifications.py

from django.core.mail import send_mail
from django.conf import settings
from datetime import date

def notify_results_published(event):
    # Check if the event has ended and today's date is the same as the event date
    if event.date == date.today():
        subject = f"Results Published for {event.title}"
        message = f"The results for the event '{event.title}' have been published."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['alvinksabu200115@gmail.com']  # Adjust as needed
        send_mail(subject, message, from_email, recipient_list)
