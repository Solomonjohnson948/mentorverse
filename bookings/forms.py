from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Profile, Review, Mentor


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'reason']

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'time': forms.TimeInput(attrs={
                'type': 'time'
            }),

            'reason': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'What do you want help with?'
            }),
        }


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    gender = forms.CharField(max_length=20)
    field = forms.ChoiceField(choices=Profile.FIELD_CHOICES)
    goal = forms.ChoiceField(choices=Profile.GOAL_CHOICES)

    class Meta:
        model = User

        fields = [
            'username',
            'full_name',
            'email',
            'gender',
            'field',
            'goal',
            'password1',
            'password2',
        ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]

        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'placeholder': 'Rate from 1 to 5'
            }),

            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this mentor...'
            }),
        }


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = [
            'name',
            'expertise',
            'bio',
            'image',
            'rating',
            'reviews',
            'company',
            'price',
            'is_featured',
        ]