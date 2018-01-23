from django.shortcuts import render
from django.core import serializers

from datetime import datetime
import pytz

from .models import Stock, Day

def index_fiavis(request):

    time_now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

    last_day_updated = Day.objects.filter(updated=True).order_by('time')[0]
    last_stocks_updated = Stock.objects.filter(day__time__startswith=last_day_updated.time.date())

    stocks = Stock.objects.all()
    stocks_json = serializers.serialize('json', stocks)

    return render(request, 'fiavis/index.html', {'last_day_updated'   : last_day_updated,
                                                 'last_stocks_updated': last_stocks_updated})