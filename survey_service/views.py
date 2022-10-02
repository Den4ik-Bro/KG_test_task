from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Survey, Answer, Color
from .forms import RegistrationUserForm, SurveyForm
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationFormView(generic.FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationUserForm

    def post(self, request, *args, **kwargs):
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            login_user = authenticate(request, username=user.username, password=form.cleaned_data['password_1'])
            login(request, login_user)
            return redirect(reverse('survey_service:home'))
        return render(request, self.template_name, context={'form': form})


class HomeView(generic.TemplateView):
    template_name = 'survey_service/home.html'


class SurveyListView(generic.ListView):
    queryset = Survey.objects.all()
    template_name = 'survey_service/all_surveys.html'
    context_object_name = 'surveys'


class SurveyDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Survey.objects.all()
    template_name = 'survey_service/detail_survey.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        questions = self.get_object().question_set.all()
        context = super(SurveyDetailView, self).get_context_data()
        context['form'] = SurveyForm(questions)
        return context

    def post(self, request, *args, **kwargs): # подумать над этой логикой
        survey = self.get_object()
        questions = survey.question_set.all()
        user = request.user
        form = SurveyForm(questions, request.POST)
        if form.is_valid():
            if survey in user.passed_surveys.all():
                return redirect(reverse('survey_service:survey_passed'))
            correct = 0
            for value in form.cleaned_data.values():
                answer = Answer.objects.get(pk=int(value))
                if answer.correct:
                    correct += 1
            if correct == len(form.cleaned_data):
                user.currency += survey.point
                user.passed_surveys.add(survey)
                user.save()
                return redirect(reverse('survey_service:survey_passed'))
        return redirect(reverse('survey_service:survey_failed'))


class SurveyPassedView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'survey_service/survey_passed.html'

    def get_context_data(self, **kwargs):
        context = super(SurveyPassedView, self).get_context_data()
        context['point'] = self.request.user.currency
        return context


class SurveyFailedView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'survey_service/survey_failed.html'


class ProfileListView(generic.ListView):
    queryset = User.objects.all()
    context_object_name = 'users'
    template_name = 'survey_service/profile_list.html'


class ProfileDetailView(generic.DetailView):
    template_name = 'survey_service/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()
        context['tests'] = self.request.user.passed_surveys.all()
        context['color'] = self.request.user.color
        return context


class ColorListView(generic.ListView):
    queryset = Color.objects.all()
    template_name = 'survey_service/colors.html'
    context_object_name = 'colors'


class BuyColorView(generic.View):

    def post(self, request, *args, **kwargs):
        user = request.user
        color = get_object_or_404(Color, pk=kwargs['pk'])
        if user.currency >= color.price and user.color != color.color:
            user.currency -= color.price
            user.color = color.color
            user.save()
            return redirect(reverse('survey_service:profile', kwargs={'pk': request.user.pk}))
        return redirect(reverse('survey_service:buy_failed'))


class BuyFailedView(generic.TemplateView):
    template_name = 'survey_service/buy_failed.html'