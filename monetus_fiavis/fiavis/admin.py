from django.contrib import admin

# Register your models here.
from .models import Stock, Day

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('day', 'code', 'vcp', 'vopen', 'vhigh', 'vlow', 'vclose', 'fshare')

@admin.register(Day)
class StockAdmin(admin.ModelAdmin):
    list_display = ('time', 'vcp', 'updated')