from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Fest(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime

class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    registration_start = models.DateTimeField()
    results_published = models.BooleanField(default=False)
    fest = models.ForeignKey('Fest', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add prize fields
    prize_1st = models.ManyToManyField('Registration', related_name='prize_1st', blank=True)
    prize_2nd = models.ManyToManyField('Registration', related_name='prize_2nd', blank=True)
    prize_3rd = models.ManyToManyField('Registration', related_name='prize_3rd', blank=True)

    def is_full(self):
        return self.capacity <= self.registrations.count()

    def has_started(self):
        event_datetime = datetime.combine(self.date, self.time)
        event_datetime = timezone.make_aware(event_datetime)
        return timezone.now() >= event_datetime

    def has_ended(self):
        event_datetime = datetime.combine(self.date, self.time)
        event_datetime = timezone.make_aware(event_datetime)
        return timezone.now() > event_datetime

    def __str__(self):
        return self.title

    def prize_counts(self):
        return {
            '1st': self.prize_1st.count(),
            '2nd': self.prize_2nd.count(),
            '3rd': self.prize_3rd.count()
        }

    def can_award_prizes(self):
        counts = self.prize_counts()
        return all(count <= 1 for count in counts.values()) and sum(counts.values()) < 3

    def clean(self):
        super().clean()
        if self.fest:
            if not (self.fest.start_date <= self.date <= self.fest.end_date):
                raise ValidationError({
                    'date': 'Event date must be within the fest date range.'
                })
        else:
            raise ValidationError({
                'fest': 'Event must be associated with a valid fest.'
            })

        event_datetime = datetime.combine(self.date, self.time)
        event_datetime = timezone.make_aware(event_datetime)
        if self.registration_start >= event_datetime:
            raise ValidationError({
                'registration_start': 'Registration start time must be before the event start time.'
            })

    def save(self, *args, **kwargs):
        # Update the event status before saving
        if self.has_started():
            self.status = 'approved'
        if self.has_ended():
            self.status = 'completed'
        super().save(*args, **kwargs)

class Registration(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    token = models.CharField(max_length=10)
    prize = models.CharField(max_length=10, choices=[('', 'No Prize'), ('1st', '1st Prize'), ('2nd', '2nd Prize'), ('3rd', '3rd Prize')], default='')
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Prize(models.Model):
    PRIZE_CHOICES = [
        ('first', 'First Prize'),
        ('second', 'Second Prize'),
        ('third', 'Third Prize'),
    ]
    event = models.ForeignKey(Event, related_name='prizes', on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, related_name='prizes', on_delete=models.CASCADE)
    prize_type = models.CharField(max_length=10, choices=PRIZE_CHOICES)

    def clean(self):
        super().clean()
        # Ensure the same registration is not assigned multiple prizes for the same event
        if Prize.objects.filter(event=self.event, registration=self.registration).exclude(pk=self.pk).exists():
            raise ValidationError("A registration cannot be awarded multiple prizes for the same event.")


class FrontPageVideo(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='front_page_videos/')

    def __str__(self):
        return self.title

class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    overall_rating = models.CharField(max_length=20)
    content_relevance = models.CharField(max_length=30)
    speaker_evaluation = models.CharField(max_length=20)
    organization_rating = models.CharField(max_length=30)
    suggestions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exported_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"Feedback from {self.user.username} for {self.event.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)
    

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"Profile for {self.user.username}"
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)


class CollegePoster(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posters/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class EventPhoto(models.Model):
    image = models.ImageField(upload_to='event_photos/')
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.description or "No description"