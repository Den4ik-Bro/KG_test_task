from django.urls import path
from . import views


app_name = 'survey_service'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('tests/', views.TestListView.as_view(), name='all_tests'),
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='detail_test'),
    path('test_passed', views.TestPassed.as_view(), name='test_passed'),
    path('test_failed', views.TestFailed.as_view(), name='test_failed'),
]