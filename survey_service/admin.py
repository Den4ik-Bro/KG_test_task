from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Survey, Question, Answer, Color


User = get_user_model()

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Color)
admin.site.register(User)