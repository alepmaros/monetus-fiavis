from django.shortcuts import render
from django.core import serializers

from datetime import datetime
import pytz

from .models import Stock, Day

def index_fiavis(request):

    time_now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

    last_day_updated = Day.objects.filter(updated=True).order_by('time')[0]
    last_stocks_updated = Stock.objects.filter(day__time__startswith=last_day_updated.time.date())

    all_days = Day.objects.all()
    all_stocks = Stock.objects.all()

    all_days_json = serializers.serialize('json', all_days)
    all_stocks_json = serializers.serialize('json', all_stocks)

    return render(request, 'fiavis/index.html', {'all_days'   : all_days_json,
                                                 'all_stocks' : all_stocks_json,
                                                 'last_stocks_updated'   : last_stocks_updated,
                                                 'last_day_updated'      : last_day_updated})