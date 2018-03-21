import json, requests, simplejson, os, time, config
from pprint import pprint
from alpha_vantage.timeseries import TimeSeries
import urllib.request

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
    print(company)
    try:
        ts = TimeSeries(key = config.api_key)
        data, meta_data = ts.get_daily(company + '.SA')
        today = time.strftime("%Y-%m-%d")
        print(data[today])
        response = {
            'valid': 0,
            'cp': (float(data[today]['4. close']) * 100 / float(data[today]['1. open'])) - 100,
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
print(get_all_stocks())