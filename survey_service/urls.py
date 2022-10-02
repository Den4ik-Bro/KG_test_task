from django.urls import path
from . import views


app_name = 'survey_service'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('tests/', views.SurveyListView.as_view(), name='all_surveys'),
    path('test/<int:pk>/', views.SurveyDetailView.as_view(), name='detail_survey'),
    path('test_passed', views.SurveyPassedView.as_view(), name='survey_passed'),
    path('test_failed', views.SurveyFailedView.as_view(), name='survey_failed'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile')
]