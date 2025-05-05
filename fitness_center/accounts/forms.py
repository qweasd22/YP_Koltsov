from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'phone',
            'full_name',
            'birth_date',
            'gender',
            'photo',
            'password1',
            'password2',
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # добавляем классы Bootstrap к полям пароля и текстовым полям
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['TextInput', 'PasswordInput', 'NumberInput']:
                field.widget.attrs.setdefault('class', 'form-control')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'birth_date', 'gender', 'goal', 'experience_years', 'achievements', 'photo']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
