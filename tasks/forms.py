from django.forms import ModelForm
from .models import Task
from django import forms

class Create_Task_Form(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo','descripcion','important']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder': 'Write a tittle'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }