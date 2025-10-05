from django.contrib import admin
from .models import UserProfile, Project, Objective, DailyCheckIn, Tip, Hobby


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'scheduling_method', 'created_at']
    search_fields = ['user__username', 'goal']
    list_filter = ['scheduling_method']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'start_date', 'due_date']
    search_fields = ['name', 'user__username']
    list_filter = ['is_active', 'start_date']


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'date', 'is_completed', 'project']
    search_fields = ['description', 'user__username']
    list_filter = ['is_completed', 'date']


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood', 'created_at']
    search_fields = ['user__username']
    list_filter = ['mood', 'date']


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['category', 'source', 'content']
    search_fields = ['source', 'content']
    list_filter = ['category']


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'created_at']
    search_fields = ['name', 'user__username']
