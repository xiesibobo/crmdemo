from django.contrib import admin


# Register your models here.
from . import models
admin.site.register(models.UserInfo)
admin.site.register(models.ClassList)
admin.site.register(models.Student)
admin.site.register(models.Questionnaire)
admin.site.register(models.Questions)
admin.site.register(models.Option)
admin.site.register(models.Answer)