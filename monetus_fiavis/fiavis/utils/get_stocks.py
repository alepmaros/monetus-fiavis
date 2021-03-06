import json, requests, simplejson, os
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
import urllib.request
import pytz

def get_all_stocks():
    f = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    companies = json.load(open(f + '/utils/stocks.json'))

    for x in range(0, len(companies['stocks'])):
        companystatus = get_company_status(companies['stocks'][x]['code'])

        companies['stocks'][x]['status'] = companystatus

    return (companies)

# valid: 0 caso seja um retorno válido
# valid: 1 caso haja uma falha na API
def get_company_status(company):
    try:
        ts = TimeSeries(key=os.environ['ALPHA_KEY'])
        data, meta_data = ts.get_daily(company + '.SA')
        today = datetime.strftime(datetime.now(tz=pytz.timezone("America/Sao_Paulo")), '%Y-%m-%d')

        if date.today().weekday() == 0:
            last_day = datetime.strftime(datetime.now(tz=pytz.timezone("America/Sao_Paulo")) - timedelta(3), '%Y-%m-%d')
        else:
            last_day = datetime.strftime(datetime.now(tz=pytz.timezone("America/Sao_Paulo")) - timedelta(1), '%Y-%m-%d')
        
        response = {
            'valid': 0,
            'cp': float("{0:.2f}".format(((float(data[today]['4. close']) * 100 / float(data[last_day]['4. close'])) - 100.0))),
            'op': float(data[today]['1. open']),
            'hi': float(data[today]['2. high']),
            'lo': float(data[today]['3. low']),
            'l': float(data[today]['4. close'])
        }

    except:
        response = {
            'valid': 1
        }

    return response