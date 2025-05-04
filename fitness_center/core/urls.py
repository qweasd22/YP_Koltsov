from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('request/new/', views.create_request, name='create_request'),
    path('request/<int:pk>/process/', views.process_request, name='process_request'),
    path('request/<int:pk>/plan/new/', views.create_training_plan, name='create_training_plan'),
    path('plan/<int:plan_id>/', views.training_plan_view, name='training_plan'),
    path('today/', views.today_workouts, name='today_workouts'),
    path('session/<int:pk>/update/', views.update_session, name='update_session'),
    path('trainer/clients/', views.trainer_clients, name='trainer_clients'),
    path('requests/', views.client_requests, name='client_requests'),
    # Создать новую заявку
    path('request/new/', views.create_request, name='create_request'),
    path('trainer/requests/', views.trainer_requests, name='trainer_requests'),
    # Обработка конкретной заявки (принять/отклонить)
    path('request/<int:pk>/process/', views.process_request, name='process_request'),
    # Создание плана после принятия заявки
    path('request/<int:pk>/plan/new/', views.create_training_plan, name='create_training_plan'),
    path('requests/', views.client_requests, name='client_requests'),
    # Создать новую заявку
    path('request/new/', views.create_request, name='create_request'),
    
    # --- Trainer URLs ---
    # Список заявок тренера
    path('trainer/requests/', views.trainer_requests, name='trainer_requests'),
    # Обработка конкретной заявки (принять/отклонить)
    path('request/<int:pk>/process/', views.process_request, name='process_request'),
    # Создание плана после принятия заявки
    path('request/<int:pk>/plan/new/', views.create_training_plan, name='create_training_plan'),

    # --- General schedule URLs ---
    path('plan/<int:plan_id>/', views.training_plan_view, name='training_plan'),
    path('today/', views.today_workouts, name='today_workouts'),
    path('session/<int:pk>/update/', views.update_session, name='update_session'),

    # --- Trainer dashboard ---
    path('trainer/clients/', views.trainer_clients, name='trainer_clients'),

    # Список тренеров (для клиента)
    path('trainers/', views.trainer_list, name='trainer_list'),
]