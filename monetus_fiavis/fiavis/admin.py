from django.contrib import admin

# Register your models here.
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'time', 'vcp', 'vopen', 'vhigh', 'vlow', 'vclose', 'fshare')