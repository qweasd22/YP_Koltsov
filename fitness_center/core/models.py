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

class Discount(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'}
    )
    percent = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    trainers = models.ManyToManyField(
        User,
        limit_choices_to={'role': 'trainer'},
        through='TrainerCourse'
    )

class TrainerCourse(models.Model):
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'trainer'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

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