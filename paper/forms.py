from django import forms
from .models import Subject, Question

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'duration_minutes']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Enter time in minutes'}),
        }
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
        ]
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter question here',
                'rows': 3
            }),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm1(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
