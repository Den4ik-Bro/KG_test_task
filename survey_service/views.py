from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from .models import Test, Answer
from .forms import RegistrationUserForm, TestForm, BuyColorForm
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


class TestListView(generic.ListView):
    queryset = Test.objects.all()
    template_name = 'survey_service/all_tests.html'
    context_object_name = 'tests'


class TestDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Test.objects.all()
    template_name = 'survey_service/detail_test.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        questions = self.get_object().question_set.all()
        context = super(TestDetailView, self).get_context_data()
        context['form'] = TestForm(questions)
        return context

    def post(self, request, *args, **kwargs): # подумать над этой логикой
        test = self.get_object()
        questions = test.question_set.all()
        user = request.user
        form = TestForm(questions, request.POST)
        if form.is_valid():
            if test in user.passed_tests.all():
                return redirect(reverse('survey_service:test_passed'))
            correct = 0
            for value in form.cleaned_data.values():
                answer = Answer.objects.get(pk=int(value))
                if answer.correct:
                    correct += 1
            if correct == len(form.cleaned_data):
                user.currency += test.point
                user.passed_tests.add(test)
                user.save()
                return redirect(reverse('survey_service:test_passed'))
        return redirect(reverse('survey_service:test_failed'))


class TestPassed(LoginRequiredMixin, generic.TemplateView):
    template_name = 'survey_service/test_passed.html'

    def get_context_data(self, **kwargs):
        context = super(TestPassed, self).get_context_data()
        context['point'] = self.request.user.currency
        return context


class TestFailed(LoginRequiredMixin, generic.TemplateView):
    template_name = 'survey_service/test_failed.html'


class ProfileView(generic.DetailView):
    template_name = 'survey_service/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['tests'] = self.request.user.passed_tests.all()
        context['color'] = self.request.user.color
        context['form'] = BuyColorForm()
        return context

    def post(self, request, *args, **kwargs):
        form = BuyColorForm(request.POST)
        user = request.user
        print(request.POST)
        if form.is_valid():
            print('ok')
        print(form.errors)
        return redirect(reverse('survey_service:profile', kwargs={'pk': request.user.pk}))
