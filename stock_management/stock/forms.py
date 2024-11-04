from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Store
from .models import UserProfile  
from .models import Stock


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please use a different email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

# Define choices for the star rating (1 to 5 stars)
STAR_CHOICES = [
    ('1', '1 Star'),
    ('2', '2 Stars'),
    ('3', '3 Stars'),
    ('4', '4 Stars'),
    ('5', '5 Stars'),
]

class FeedbackForm(forms.Form):
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'maxlength': '500', 
            'placeholder': 'Type your feedback here...',
            'class': 'feedback-textarea'
        }),
        label='Your Feedback',
        max_length=500
    )

    star = forms.ChoiceField(
        choices=STAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label='Rate Us'
    )

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'owner_name', 'email', 'phone', 'location', 'description']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone','address']
