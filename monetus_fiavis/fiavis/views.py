from django.shortcuts import render
from django.core import serializers

from datetime import datetime
import pytz

from .models import Stock

def index_fiavis(request):

    time_now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
    stocks_today = Stock.objects.filter(time__startswith=time_now.date()).order_by('-fshare')

    # valorizacao total do fundo
    fcp = 0
    for s in stocks_today:
        fcp += ( s.fshare / 100.0 ) * s.vcp

    stocks = Stock.objects.all()
    stocks_json = serializers.serialize('json', stocks)

    return render(request, 'fiavis/index.html', {'fcp'         : fcp,
                                                 'stocks_today': stocks_today,
                                                 'stocks'      : stocks_json})