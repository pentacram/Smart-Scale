from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    age = forms.CharField(widget=forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }))
    class Meta:
        model = InfoFields
        fields = ['age', 'gender', 'breed', 'feed', 'special_case']
        widgets = {
            "gender": forms.Select(attrs={"class": "form-control"}),
            "breed": forms.TextInput(attrs={"class": "form-control"}),
            "feed": forms.TextInput(attrs={"class": "form-control"}),
            "special_case": forms.Select(attrs={"class": "form-control"}),
            "age": forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            })
        }
        labels = {
            'age': "Yası",
            'gender': 'Cinsiyyət',
            'breed': "Cins",
            'feed': "Yem",

        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }
    ))

class EditForm(forms.ModelForm):
    age = forms.CharField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-target': '#datetimepicker1'
    }))
    class Meta:
        model = InfoFields
        fields = ['age', 'weight', 'breed', 'feed', 'special_case']
        widgets = {
            "age": forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "breed": forms.TextInput(attrs={"class": "form-control"}),
            "feed": forms.TextInput(attrs={"class": "form-control"}),
            "weight": forms.TextInput(attrs={"class": "form-control", 'readonly': 'asds'}),
        }
        labels = {
            'age': "Yası",
            'gender': 'Cinsiyyət',
            'breed': "Cins",
            'feed': "Yem",
            'weight': 'Çəki',
        }


class TableForm(forms.ModelForm):
    class Meta:
        fields = ["create_date", 'weight']
