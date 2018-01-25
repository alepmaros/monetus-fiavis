from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from datetime import datetime
from collections import OrderedDict
import json, requests, simplejson
import pytz
import os

from alpha_vantage.timeseries import TimeSeries

from fiavis.models import Stock, Day

def get_daily_stocks(company, share):

    ts = TimeSeries(key=os.environ['ALPHA_KEY'])
    # Alpha Vantage requires the .SA after
    data, meta_data = ts.get_daily(symbol=company+'.SA', outputsize='compact')

    # Sorting by date and only getting the x last days
    data = OrderedDict(sorted(data.items()))
    for k in range(len(data) - 19) : data.popitem(last = False)
    data.popitem(last=True)
    all_days = []
    
    for a in data:
        time = datetime.strptime(a, '%Y-%m-%d')
        time = time.replace(tzinfo=pytz.timezone("America/Sao_Paulo"))

        all_days.append(time)
        vopen  = float(data[a]['1. open'])
        vhigh  = float(data[a]['2. high'])
        vlow   = float(data[a]['3. low'])
        vclose = float(data[a]['4. close'])
        if (vopen != 0):
            vcp = ((vclose - vopen) * 100.0) / vopen
            # Probably should use Decimal here
            vcp = float("{0:.2f}".format(round(vcp,2)))
        else:
            vcp = 0.0

        try:
            day = Day.objects.get(time__startswith=time.date())
            day.time = time
            day.save()
        except ObjectDoesNotExist:
            day = Day(time=time)
            day.save()
        
        try:
            stock = Stock.objects.get(code=company, day__time__startswith=time.date())
            stock.fshare = share
            stock.vopen  = vopen
            stock.vhigh  = vhigh
            stock.vlow   = vlow
            stock.vclose = vclose
            stock.vcp    = vcp
        except ObjectDoesNotExist:
            stock = Stock(code=company, vcp=vcp,
                vopen = vopen, vhigh = vhigh, vlow = vlow,
                vclose = vclose, fshare = share, day=day)
        stock.save()

    return all_days

class Command(BaseCommand):
    help = 'Populate the database with a few days'

    def handle(self, *args, **options):
        all_days = []

        companies = json.load(open(settings.BASE_DIR + '/fiavis/utils/stocks.json'))

        for x in range(0, len(companies['stocks'])):
                self.stdout.write("Getting stocks for: %s" % companies['stocks'][x]['code'], ending='\n')
                all_days = get_daily_stocks(companies['stocks'][x]['code'], float(companies['stocks'][x]['share']))


        self.stdout.write("Calculating vcp for all days", ending='\n')
        for d in all_days:
            day = Day.objects.get(time__startswith=d.date())
            if Stock.objects.filter(day=day).count() > 0:
                    vcp = 0.0
                    for stock in Stock.objects.filter(day=day):
                        vcp += stock.vcp * (stock.fshare / 100.0)

                    # Probably should use Decimal here instead
                    day.vcp = float("{0:.2f}".format(round(vcp,2)))
                    day.updated = True
                    day.save()
        
        self.stdout.write(self.style.SUCCESS('Done.'))