from django import forms
from django.contrib.auth.models import User

from MovieHub_app.models import Review


class UserCreateForm(forms.ModelForm):
    password_confirmation = forms.CharField(label="Password confirmation",
                                            widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation')
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
        }

    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != \
                self.cleaned_data['password_confirmation']:
            raise forms.ValidationError('The provided passwords are different.')


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['movie', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': '4',
                'placeholder': 'Write your review',
                'class': 'form-control',
            }),
        }