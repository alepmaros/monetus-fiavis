from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from fiavis.models import Stock, Day

class Command(BaseCommand):
    help = 'Recalculate vcp for manual modificaitons on db'

    def handle(self, *args, **options):

        self.stdout.write("Recalculating all vcps", ending='\n')
        
        all_days = Day.objects.filter(updated=True).prefetch_related('stock_set').order_by('time')
        for day in all_days:
            self.stdout.write("Calculating vcp for day " + day.time.strftime("%Y-%m-%d %H:%M:%S"), ending='\n')
            vcp = 0.0
            stocks = day.stock_set.all()
            for s in stocks:
                vcp += s.vcp * (s.fshare / 100.0)

            day.vcp = float("{0:.2f}".format(round(vcp,2)))
            day.save()
        
        self.stdout.write(self.style.SUCCESS('Done.'))