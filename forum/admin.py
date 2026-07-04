from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Theme, Answer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('avatar',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('avatar',)}),
    )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('theme', 'author', 'created_at')
    list_filter = ('created_at',)