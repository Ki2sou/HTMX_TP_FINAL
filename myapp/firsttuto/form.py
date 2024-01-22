from django import forms
from django.contrib.auth.forms import UserCreationForm
from firsttuto.models import User, Task

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']