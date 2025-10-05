from django.urls import path
from . import views

urlpatterns = [
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('daily-plan/', views.daily_plan_view, name='daily_plan'),
    path('objectives/', views.objectives_list_view, name='objectives_list'),
    path('objectives/<int:pk>/', views.objective_update_view, name='objective_update'),
    path('daily-checkin/', views.daily_checkin_view, name='daily_checkin'),
    path('tips/random/', views.random_tip_view, name='random_tip'),
    path('suggestions/hobby/', views.hobby_suggestion_view, name='hobby_suggestion'),
    path('suggestions/workout/', views.workout_plan_view, name='workout_plan'),
    path('projects/', views.ProjectListCreateView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('hobbies/', views.HobbyListCreateView.as_view(), name='hobby_list'),
    path('hobbies/<int:pk>/', views.HobbyDetailView.as_view(), name='hobby_detail'),
]
