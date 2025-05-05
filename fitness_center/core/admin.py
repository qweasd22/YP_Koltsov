from django.contrib import admin
from .models import (
    TrainerProfile, Discount, Course, TrainerCourse,
    ClientRequest, TrainingPlan, Exercise,
    IndividualWorkout, WorkoutSession
)

admin.site.register(TrainerProfile)


admin.site.register(ClientRequest)
admin.site.register(TrainingPlan)
admin.site.register(Exercise)
admin.site.register(IndividualWorkout)
admin.site.register(WorkoutSession)

from django.contrib import admin
from .models import Course, TrainerCourse, Discount
from accounts.models import User

# Inline для курсов тренера


# Регистрируем модели для админки
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(TrainerCourse)
class TrainerCourseAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'course', 'assigned_at')
    list_filter = ('assigned_at', 'course')
    autocomplete_fields = ('trainer', 'course')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('client', 'percent', 'valid_until')
    list_filter = ('valid_until',)
    autocomplete_fields = ('client',)

# Регистрируем кастомную модель User
