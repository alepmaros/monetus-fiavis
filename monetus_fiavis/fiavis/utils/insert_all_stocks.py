import json
import os

from fiavis.models import Day, Stock

def insert_all_stocks(day):
    '''
    Insert all stocks for that day and initialize with 0 on the table
    '''
    f = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    companies = json.load(open(f + '/utils/stocks.json'))

    for x in range(0, len(companies['stocks'])):
        company_code = companies['stocks'][x]['code']
        company_share = companies['stocks'][x]['share']

        stock = Stock(code=company_code, vcp=0,
                        vopen = 0, vhigh = 0, vlow = 0,
                        vclose = 0, fshare = company_share, day=day)
        stock.save()