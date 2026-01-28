from django.contrib import admin
from .models import Expense
# Register your models here.
admin.site.site_header = "Expense Tracker Admin"
admin.site.register(Expense)
