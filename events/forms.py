from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event, Registration, TeamMember, Profile
from django.core.exceptions import ValidationError
from .models import Department
from .models import Fest
from .models import CollegePoster
from .models import ContactMessage
from .models import Profile
from .models import FrontPageVideo


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'email'] 

class FestForm(forms.ModelForm):
    class Meta:
        model = Fest
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'capacity', 'registration_start', 'department', 'fest']
        widgets = {
            'registration_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'fest': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'min': '', 'max': ''})  # Set empty initially

        if 'fest' in self.data:
            try:
                fest_id = int(self.data.get('fest'))
                fest = Fest.objects.get(pk=fest_id)
                self.fields['date'].widget.attrs.update({
                    'min': fest.start_date.strftime('%Y-%m-%d'),
                    'max': fest.end_date.strftime('%Y-%m-%d')
                })
            except (ValueError, TypeError, Fest.DoesNotExist):
                pass  # Invalid input or no fest selected
        elif self.instance.pk and self.instance.fest:
            fest = self.instance.fest
            self.fields['date'].widget.attrs.update({
                'min': fest.start_date.strftime('%Y-%m-%d'),
                'max': fest.end_date.strftime('%Y-%m-%d')
            })


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['event', 'user', 'name', 'email', 'token', 'prize']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.event.has_ended():
            self.fields['prize'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        prize = cleaned_data.get('prize')
        event = cleaned_data.get('event')

        # Check if registration period has started
        if event and timezone.now() < event.registration_start:
            raise ValidationError("Registration has not started for this event yet.")

        if prize and event:
            if prize != '':
                if not event.can_award_prizes():
                    raise ValidationError("Cannot award more prizes. The event already has 3 prizes assigned.")
                if event.registrations.filter(prize=prize).exists():
                    raise ValidationError(f"The prize '{prize}' has already been awarded.")

        return cleaned_data

class EventRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email', widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    confirm_registration = forms.BooleanField(required=True, label='I confirm that I want to register for this event')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FeedbackForm(forms.Form):
    overall_rating = forms.ChoiceField(
        choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')],
        widget=forms.RadioSelect,
        label='How would you rate the overall quality of the event?'
    )
    content_relevance = forms.ChoiceField(
        choices=[('Very relevant', 'Very relevant'), ('Somewhat relevant', 'Somewhat relevant'), ('Neutral', 'Neutral'), ('Not very relevant', 'Not very relevant'), ('Not relevant at all', 'Not relevant at all')],
        widget=forms.RadioSelect,
        label='How relevant was the content of the event to your interests or needs?'
    )
    speaker_evaluation = forms.ChoiceField(
        choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')],
        widget=forms.RadioSelect,
        label='How would you rate the speaker(s)/presenter(s) in terms of knowledge and presentation skills?'
    )
    organization_rating = forms.ChoiceField(
        choices=[('Very well organized', 'Very well organized'), ('Well organized', 'Well organized'), ('Neutral', 'Neutral'), ('Poorly organized', 'Poorly organized'), ('Very poorly organized', 'Very poorly organized')],
        widget=forms.RadioSelect,
        label='How well was the event organized? (e.g., scheduling, venue, materials)'
    )
    suggestions = forms.CharField(
        widget=forms.Textarea,
        label='What suggestions do you have for improving future events? (Please provide details)',
        required=False
    )

class ReplyForm(forms.Form):
    reply_message = forms.CharField(widget=forms.Textarea, label='Reply Message')

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'image']

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError("This email address is already in use. Please use a different email address.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
class CollegePosterForm(forms.ModelForm):
    class Meta:
        model = CollegePoster
        fields = ['title', 'image'] 

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']  # Ensure these fields match the ContactMessage model

from django import forms
from django.core.exceptions import ValidationError
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('A profile with this email already exists.')
        return email


class FrontPageVideoForm(forms.ModelForm):
    class Meta:
        model = FrontPageVideo
        fields = ['title', 'video']


from django import forms
from .models import Event, Registration

class SelectEventForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        empty_label="Select an event",
        label="Select Event"
    )

class SelectWinnersForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    first_prize = forms.ModelChoiceField(
        queryset=Registration.objects.none(),
        required=False,
        label='First Prize'
    )
    second_prize = forms.ModelChoiceField(
        queryset=Registration.objects.none(),
        required=False,
        label='Second Prize'
    )
    third_prize = forms.ModelChoiceField(
        queryset=Registration.objects.none(),
        required=False,
        label='Third Prize'
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        if event:
            self.fields['event_id'].initial = event.id
            registrations = Registration.objects.filter(event=event)
            for field in ['first_prize', 'second_prize', 'third_prize']:
                self.fields[field].queryset = registrations

    def clean(self):
        cleaned_data = super().clean()
        winners = [
            cleaned_data.get('first_prize'),
            cleaned_data.get('second_prize'),
            cleaned_data.get('third_prize')
        ]
        winners = [w for w in winners if w]
        if len(winners) != len(set(winners)):
            raise forms.ValidationError("A person cannot be selected for more than one prize.")
        return cleaned_data


from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
    }))



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from .models import NewsItem

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

from django import forms
from .models import EventPhoto

class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ['title', 'description', 'photo'] 