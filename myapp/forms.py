from django import forms
from .models import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Input Username'
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Input Password'
        }
    ))
    class Meta:
        model = CustomUser
        fields = ['username','password']

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Input Username'
            }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
            attrs={
               'class' : 'form-control',
                'placeholder' : 'Input Email'
            }
    ))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Input Password'
        }
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Confirm Password'
        }
    ))

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']
        # fields = ('__all__')

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title','description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz' , 'question']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question','option','is_correct']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['Name','Class','Age','Institution']