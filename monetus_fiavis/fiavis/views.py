from django.shortcuts import render
from django.core import serializers

from datetime import datetime
import pytz

from .models import Stock, Day


def index_fiavis(request):

    time_now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

    last_day_updated = Day.objects.filter(updated=True).order_by('-time')[0]
    last_stocks_updated = Stock.objects.filter(day__time__startswith=last_day_updated.time.date())

    all_days = Day.objects.all().order_by('time')
    all_stocks = all_days[2].stock_set.all()
    all_days_object = []
    for d in all_days:
        sd = {
            'day': d.time,
            'vcp': d.vcp,
            'stocks': serializers.serialize('json', d.stock_set.all(), fields=('code', 'vcp') )
        }
        all_days_object.append(sd)

    return render(request, 'fiavis/index.html', {'all_days'   : all_days_object,
                                                 'last_stocks_updated'   : last_stocks_updated,
                                                 'last_day_updated'      : last_day_updated})