from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView
from core.views import profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]
