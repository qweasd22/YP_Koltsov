from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

class TrainerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'trainer'},
        related_name='trainer_profile'
    )
    experience_years = models.PositiveSmallIntegerField()
    achievements = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.experience_years} лет)"

class Course(models.Model):
    title = models.CharField("Название курса", max_length=200)
    description = models.TextField("Описание курса", blank=True)

    def __str__(self):
        return self.title


class TrainerCourse(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Тренер",
        limit_choices_to={'role': 'trainer'},
        on_delete=models.CASCADE,
        related_name='trainer_courses'
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        on_delete=models.CASCADE
    )
    assigned_at = models.DateField("Дата назначения", auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'course')
        verbose_name = "Назначение курса"
        verbose_name_plural = "Назначения курсов"

    def __str__(self):
        return f"{self.trainer.full_name} → {self.course.title}"


class Discount(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Клиент",
        limit_choices_to={'role': 'client'},
        on_delete=models.CASCADE,
        related_name='discounts'
    )
    percent = models.PositiveSmallIntegerField("Процент скидки", help_text="От 1 до 100")
    valid_until = models.DateField("Действует до")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.client.full_name}: {self.percent}% до {self.valid_until}"

class ClientRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'}
    )
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests',
        limit_choices_to={'role': 'trainer'}
    )
    goal = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка {self.id}: {self.client.full_name} → {self.trainer.full_name}"

class TrainingPlan(models.Model):
    request = models.OneToOneField(ClientRequest, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class IndividualWorkout(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    frequency_per_week = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()

class WorkoutSession(models.Model):
    workout = models.ForeignKey(IndividualWorkout, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    pulse = models.PositiveSmallIntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('workout', 'date')