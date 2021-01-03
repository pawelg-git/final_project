from django.contrib import admin
from .models import *

@admin.register(Branch, PipeOrder)
class AppAdmin(admin.ModelAdmin):
    pass

# Register your models here.
