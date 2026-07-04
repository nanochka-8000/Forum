from django.urls import path
from . import views

urlpatterns = [
    path('', views.ThemeListView.as_view(), name='home'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    path('theme/create/', views.ThemeCreateView.as_view(), name='theme_create'),
    path('theme/<int:pk>/', views.ThemeDetailView.as_view(), name='theme_detail'),
    path('theme/<int:pk>/edit/', views.ThemeUpdateView.as_view(), name='theme_update'),
    path('theme/<int:pk>/delete/', views.ThemeDeleteView.as_view(), name='theme_delete'),

    path('theme/<int:theme_pk>/answer/', views.AnswerCreateView.as_view(), name='answer_create'),

    path('answer/<int:pk>/edit/', views.AnswerUpdateView.as_view(), name='answer_update'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer_delete'),
]