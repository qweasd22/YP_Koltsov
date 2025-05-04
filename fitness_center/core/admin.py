from django.contrib import admin
from .models import (
    TrainerProfile, Discount, Course, TrainerCourse,
    ClientRequest, TrainingPlan, Exercise,
    IndividualWorkout, WorkoutSession
)

admin.site.register(TrainerProfile)
admin.site.register(Discount)
admin.site.register(Course)
admin.site.register(TrainerCourse)
admin.site.register(ClientRequest)
admin.site.register(TrainingPlan)
admin.site.register(Exercise)
admin.site.register(IndividualWorkout)
admin.site.register(WorkoutSession)