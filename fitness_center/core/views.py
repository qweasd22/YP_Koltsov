from urllib.request import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.urls import reverse
from .models import ClientRequest, TrainingPlan, WorkoutSession
from .forms import ClientRequestForm, WorkoutSessionForm
from datetime import date, timedelta

User = get_user_model()

@login_required
def dashboard(request):
    # Клиенту — его заявки
    if request.user.role == 'client':
        return redirect('core:client_requests')
    # Тренеру — его новые заявки
    elif request.user.role == 'trainer':
        return redirect('core:trainer_requests')
    # Администратору — в админку Django
    elif request.user.role == 'admin':
        return redirect(reverse('admin:index'))
    # На всякий случай — на клиентский дашборд
    return redirect('core:client_requests')


@login_required
def trainer_list(request):
    # Только клиентам показываем список тренеров
    if request.user.role == 'client':
        trainers = User.objects.filter(role='trainer')
        return render(request, 'core/trainer_list.html', {'trainers': trainers})
    # Админу — сразу в админку
    elif request.user.role == 'admin':
        return redirect(reverse('admin:index'))
    # Всем остальным — на дашборд
    return redirect('core:dashboard')
@login_required
def create_request(request):
    # клиент отправляет заявку тренеру
    if request.user.role != 'client':
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.client = request.user
            req.save()
            return redirect('core:client_requests')
    else:
        form = ClientRequestForm(initial={'trainer': request.GET.get('trainer')})
    return render(request, 'core/create_request.html', {'form': form})

@login_required
def client_requests(request):
    # список заявок клиента
    qs = ClientRequest.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'core/client_requests.html', {'requests': qs})

@login_required
def trainer_requests(request):
    # новые заявки тренера
    qs = ClientRequest.objects.filter(trainer=request.user, status='pending')
    return render(request, 'core/trainer_requests.html', {'requests': qs})

@login_required
def process_request(request, pk):
    # тренер принимает/отклоняет заявку
    req = get_object_or_404(ClientRequest, pk=pk, trainer=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            req.status = 'accepted'
            req.save()
            return redirect('core:create_training_plan', pk=req.pk)
        elif action == 'reject':
            req.status = 'rejected'
            req.reason = request.POST.get('reason', '')
            req.save()
            return redirect('core:trainer_requests')
    return render(request, 'core/process_request.html', {'req': req})

@login_required
def create_training_plan(request, pk):
    # создание плана тренером и генерация сессий
    req = get_object_or_404(ClientRequest, pk=pk, trainer=request.user, status='accepted')
    if hasattr(req, 'trainingplan'):
        return redirect('core:training_plan', plan_id=req.trainingplan.id)
    if request.method == 'POST':
        start = request.POST['start_date']
        end = request.POST['end_date']
        plan = TrainingPlan.objects.create(request=req, start_date=start, end_date=end)
        # создаем сессии для каждого упражнения в плане на каждый день
        workouts = plan.individualworkout_set.all()
        dates = [plan.start_date + timedelta(days=i) for i in range((plan.end_date - plan.start_date).days + 1)]
        for wo in workouts:
            for d in dates:
                WorkoutSession.objects.create(workout=wo, date=d)
        return redirect('core:training_plan', plan_id=plan.id)
    return render(request, 'core/create_training_plan.html', {'req': req})

@login_required
def training_plan_view(request, plan_id):
    # просмотр плана и сегодняшних занятий
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    workouts = plan.individualworkout_set.all()
    sessions_today = WorkoutSession.objects.filter(workout__plan=plan, date=date.today())
    return render(request, 'core/training_plan.html', {
        'plan': plan,
        'workouts': workouts,
        'sessions_today': sessions_today,
    })

@login_required
def today_workouts(request):
    # список занятий на сегодня для клиента
    plans = TrainingPlan.objects.filter(request__client=request.user)
    today = date.today()
    sessions = WorkoutSession.objects.filter(date=today, workout__plan__in=plans)
    return render(request, 'core/today_workouts.html', {'sessions': sessions})

@login_required
def update_session(request, pk):
    # отметка выполнения и ввод пульса
    session = get_object_or_404(WorkoutSession, pk=pk, workout__plan__request__client=request.user)
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('core:today_workouts')
    else:
        form = WorkoutSessionForm(instance=session)
    return render(request, 'core/update_session.html', {'form': form, 'session': session})

@login_required
def trainer_clients(request):
    # дашборд тренера: список клиентов с прогрессом
    plans = TrainingPlan.objects.filter(request__trainer=request.user)
    clients_data = []
    for plan in plans:
        total_days = (plan.end_date - plan.start_date).days + 1
        done_days = WorkoutSession.objects.filter(workout__plan=plan, completed=True).count()
        percent_cycle = (done_days / total_days * 100) if total_days else 0
        total_ex = plan.individualworkout_set.count()
        done_ex = WorkoutSession.objects.filter(workout__plan=plan, completed=True).count()
        percent_ex = (done_ex / total_ex * 100) if total_ex else 0
        avg_pulse = WorkoutSession.objects.filter(workout__plan=plan, pulse__isnull=False).aggregate(Avg('pulse'))['pulse__avg'] or 0
        clients_data.append({
            'client': plan.request.client,
            'percent_cycle': percent_cycle,
            'percent_ex': percent_ex,
            'avg_pulse': avg_pulse,
        })
    return render(request, 'core/trainer_clients.html', {'clients_data': clients_data})

