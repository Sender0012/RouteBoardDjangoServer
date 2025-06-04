from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Route, RoutePoint, GameBoard

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'background']

class RoutePointForm(forms.ModelForm):
    class Meta:
        model = RoutePoint
        fields = ['x', 'y']

class GameBoardForm(forms.ModelForm):
    class Meta:
        model = GameBoard
        fields = ['title', 'rows', 'cols', 'dots']
        widgets = {
            'dots': forms.HiddenInput(),
        }