from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from imageApp.models import *

class RegisterForm(UserCreationForm):
  class Meta:
    model=CustomUserModel
    fields=['username','password1','password2']

class LoginForm(AuthenticationForm):
  pass

class UserForm(forms.ModelForm):
  class Meta:
    model=UserModel
    fields='__all__'
    exclude=['created_by']
