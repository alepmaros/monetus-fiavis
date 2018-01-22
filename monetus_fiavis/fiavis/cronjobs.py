from django_cron import CronJobBase, Schedule
from datetime import datetime
import pytz

from .utils.get_stocks import get_all_stocks

from .models import Stock

class UpdateStocksInformation(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'fiavis.update_stocks_information'

    def do(self):
        time = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

        if ( time.hour < 9 or time.hour > 19 ):
            return

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

                stock = Stock(code=s_code, time=time, vcp=s_cp,
                    vopen = s_op, vhigh = s_hi, vlow = s_lo,
                    vclose = s_l, fshare = s_share)
                stock.save()
