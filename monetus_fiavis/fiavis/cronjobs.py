from django_cron import CronJobBase, Schedule
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import pytz

from .utils.get_stocks import get_all_stocks

from fiavis.models import Stock, Day

class UpdateStocksInformation(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fiavis.update_stocks_information'

    def do(self):

        time_now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

        if ( time_now.hour < 11 or time_now.hour > 19 ):
            return

        try:
            day = Day.objects.get(time__startswith=time_now.date())
            day.time = time_now
        except ObjectDoesNotExist:
            day = Day(time=time_now)
        day.save()
            

        stocks = get_all_stocks()
        for s in stocks['stocks']:
            if (s['status']['valid'] == 0):
                s_code  = s['code']
                s_share = s['share']
                s_op = s['status']['op']
                s_hi = s['status']['hi']
                s_lo = s['status']['lo']
                s_cp = s['status']['cp']
                s_l  = s['status']['l']
                
                # If the entry already exists, update it; otherwise create a new one
                try:
                    stock = Stock.objects.get(code=s_code, day__time__startswith=time_now.date())
                    stock.fshare = s_share
                    stock.vopen  = s_op
                    stock.vhigh  = s_hi
                    stock.vlow   = s_lo
                    stock.vclose = s_l
                    stock.vcp    = s_cp
                except ObjectDoesNotExist:
                    stock = Stock(code=s_code, vcp=s_cp,
                        vopen = s_op, vhigh = s_hi, vlow = s_lo,
                        vclose = s_l, fshare = s_share, day=day)
                stock.save()

        

        # Update vcp for that day
        if Stock.objects.filter(day=day).count() > 0:
            vcp = 0.0
            for stock in Stock.objects.filter(day=day):
                vcp += stock.vcp * (stock.fshare / 100.0)

            day.vcp = vcp
            day.updated = True
            day.save()
