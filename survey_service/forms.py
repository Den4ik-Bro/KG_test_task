from django import forms
from django.contrib.auth import get_user_model
from .models import Test, Answer, Question

User = get_user_model()


class RegistrationUserForm(forms.ModelForm):
    password_1 = forms.CharField(widget=forms.PasswordInput(), label='Введите пароль')
    password_2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password_1'] != cleaned_data['password_2']:
            # raise forms.ValidationError('Пароли не совпадают')
            self.add_error('password_1', 'Пароли не совпадают')

    class Meta:
        model = User
        fields = \
            [
                'username',
                'first_name',
                'last_name',
                'email',
            ]


class TestForm(forms.Form):
    question = forms.ChoiceField(widget=forms.RadioSelect, choices=())

    def __init__(self, questions, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.questions = questions
        del self.fields['question']
        for question in questions:
            choices = [(answer.pk, answer.text ) for answer in question.answer_set.all()]
            self.fields[f'question{question.pk}'] = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
            self.fields[f'question{question.pk}'].label = question.text


class BuyColorForm(forms.Form):
    CHOICES = [
        ('green', '100'),
        ('black', '1000'),
        ('red', '700'),
        ('blue', '500'),
        ('white', '1500'),
    ]
    color = forms.MultipleChoiceField(widget=forms.RadioSelect, choices=CHOICES)