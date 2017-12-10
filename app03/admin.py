from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Boardroom)
admin.site.register(models.Record)
admin.site.register(models.Slot)
