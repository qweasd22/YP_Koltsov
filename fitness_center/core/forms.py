from django import forms
from .models import ClientRequest, WorkoutSession

class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ('trainer', 'goal')
        widgets = {
            'goal': forms.Textarea(attrs={'rows':3}),
        }

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ('completed', 'pulse')
        widgets = {
            'pulse': forms.NumberInput(attrs={'min':40, 'max':200}),
        }