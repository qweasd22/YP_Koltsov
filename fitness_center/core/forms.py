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

from .models import TrainingPlan, IndividualWorkout

TrainingPlanForm = forms.modelform_factory(
    TrainingPlan,
    fields=('start_date', 'end_date',),
    widgets={
        'start_date': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
        'end_date':   forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
    }
)

IndividualWorkoutFormSet = forms.inlineformset_factory(
    TrainingPlan, IndividualWorkout,
    fields=('exercise', 'frequency_per_week', 'sets', 'reps'),
    extra=3,  # сколько форм будет по умолчанию
    can_delete=False,
    widgets={
        'exercise':        forms.Select(attrs={'class':'form-select'}),
        'frequency_per_week': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
        'sets':            forms.NumberInput(attrs={'class':'form-control', 'min':1}),
        'reps':            forms.NumberInput(attrs={'class':'form-control', 'min':1}),
    }
)