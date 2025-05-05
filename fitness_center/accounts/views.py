from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm

class SignUpView(View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'client'  # всем новым – роль клиента
            user.save()
            login(request, user)
            return redirect('core:trainer_list')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

from django.contrib import messages
