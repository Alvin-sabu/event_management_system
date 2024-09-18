from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
import csv
from .models import Event, EventPhoto, Registration, Feedback, FrontPageVideo, Department, Fest, ContactMessage, TeamMember, Profile, CollegePoster
from .forms import RegistrationForm, ReplyForm

def notify_results_published(event):
    subject = f'Results Published for {event.title}'
    message = (
        f'The results for the event "{event.title}" have been published.\n'
        'Please log in to our website to check the results.\n'
        'Thank you for participating!'
    )
    recipient_list = [registration.email for registration in event.registrations.all()]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

class RegistrationAdmin(admin.ModelAdmin):
    form = RegistrationForm
    list_display = ('event', 'name', 'email', 'token', 'prize')
    search_fields = ('name', 'email')
    list_filter = ('event', 'prize')

    def save_model(self, request, obj, form, change):
        if change:  # If the registration is being edited
            if not obj.event.has_ended():
                raise PermissionDenied("You can only mark prizes after the event has concluded.")
            
            # Ensure the prize constraints
            if obj.prize:
                if obj.event.registrations.filter(prize=obj.prize).exists():
                    raise PermissionDenied(f"The prize '{obj.prize}' has already been awarded.")
                
                if obj.event.prize_counts().get(obj.prize, 0) >= 1:
                    raise PermissionDenied("The maximum number of awards for this prize has been reached.")
        
        super().save_model(request, obj, form, change)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'capacity')
    actions = ['notify_results']

    def notify_results(self, request, queryset):
        for event in queryset:
            if not event.has_ended():
                self.message_user(request, "Some events have not yet concluded. Notification will be sent for completed events only.")
                continue
            
            notify_results_published(event)
            self.message_user(request, f"Results notification sent for event '{event.title}'.")

    notify_results.short_description = 'Notify participants of results publication'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')

class FrontPageVideoAdmin(admin.ModelAdmin):
    list_display = ['title']

def export_feedback(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=feedback_report.csv'
    writer = csv.writer(response)
    writer.writerow([
        'Event',
        'User',
        'Overall Rating',
        'Content Relevance',
        'Speaker Evaluation',
        'Organization Rating',
        'Suggestions'
    ])
    
    for feedback in queryset:
        writer.writerow([
            feedback.event.title,
            feedback.user.username,
            feedback.overall_rating,
            feedback.content_relevance,
            feedback.speaker_evaluation,
            feedback.organization_rating,
            feedback.suggestions or ''  # Handle empty suggestions
        ])
    
    return response

export_feedback.short_description = 'Export selected feedback to CSV'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'overall_rating', 'content_relevance', 'speaker_evaluation', 'organization_rating')
    list_filter = ('event', 'user', 'overall_rating')
    search_fields = ('event__title', 'user__username')
    actions = [export_feedback]

from django.contrib import admin
from .models import ContactMessage, Event
from .forms import ReplyForm

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'replied')
    change_form_template = 'admin/contactmessage_change_form.html'
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if request.method == 'POST':
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply_message = reply_form.cleaned_data['reply_message']
                subject = f'Re: {obj.message[:30]}...'  # Subject based on the original message
                message = (
                    f'Dear {obj.name},\n\n'
                    f'Thank you for reaching out to us. Here is our reply to your query:\n\n'
                    f'Original Message: {obj.message}\n\n'
                    f'Reply: {reply_message}\n\n'
                    'Best regards,\n'
                    'Event Hub,\n'
                    'Marian College Kuttikkanam'
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # Replace with your admin email
                    [obj.email]
                )
                obj.replied = True
                obj.save()
                self.message_user(request, 'Reply sent successfully!')
                return HttpResponseRedirect(".")
        else:
            reply_form = ReplyForm()

        extra_context['reply_form'] = reply_form
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

from .models import NewsItem

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ('description', 'image')

admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(Fest)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(FrontPageVideo, FrontPageVideoAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(TeamMember)
admin.site.register(Profile)
admin.site.register(CollegePoster)
