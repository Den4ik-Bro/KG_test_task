from django.urls import path
from . import views


app_name = 'survey_service'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('surveys/', views.SurveyListView.as_view(), name='all_surveys'),
    path('survey/<int:pk>/', views.SurveyDetailView.as_view(), name='detail_survey'),
    path('survey_passed', views.SurveyPassedView.as_view(), name='survey_passed'),
    path('survey_failed', views.SurveyFailedView.as_view(), name='survey_failed'),
    path('profiles', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('colors/', views.ColorListView.as_view(), name='colors'),
    path('buy_color/<int:pk>/', views.BuyColorView.as_view(), name='buy_color'),
    path('buy_failed/', views.BuyFailedView.as_view(), name='buy_failed'),
]