from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Record)
admin.site.register(models.UploadedFile)
