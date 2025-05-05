from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from core.models import TrainerProfile, TrainerCourse, Discount


class TrainerCourseInline(admin.TabularInline):
    model = TrainerCourse
    extra = 1
    autocomplete_fields = ['course']

# Inline для скидок клиента
class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1
    autocomplete_fields = ['client']
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Персональное', {'fields': ('full_name', 'birth_date', 'gender', 'photo')}),
        ('Роли и права', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('phone', 'full_name')
    filter_horizontal = []
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.role == 'trainer':
            # Для тренера отображаем дополнительные поля
            form.base_fields['experience_years'].required = True
            form.base_fields['achievements'].required = True
        if obj and obj.role == 'client':
            # Для клиента отображаем другие поля
            form.base_fields['goal'].required = True
        return form