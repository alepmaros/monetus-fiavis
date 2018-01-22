import json, requests, simplejson
import os
from pprint import pprint

def get_all_stocks():
    f = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    companies = json.load(open(f + '/utils/stocks.json'))

    for x in range(0, len(companies['stocks'])):
        companystatus = get_company_status(companies['stocks'][x]['code'])

        companies['stocks'][x]['status'] = companystatus

    return (companies)

# valid: 0 caso seja um retorno válido
# valid: 1 caso algum atributo do objeto
# valid: 2 caso haja uma falha na API
def get_company_status(company):
    rsp = requests.get('https://finance.google.com/finance?q=' + company + '&output=json')

    if (rsp.status_code == 200):
        try:
            company_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))

            response = {
                'valid': 0,
                'cp': float(company_data['cp']) / 100,
                'l': float(company_data['l']),
                'op': float(company_data['op']),
                'hi': float(company_data['hi']),
                'lo': float(company_data['lo'])
            }

        except:
            response = {
                'valid': 1
            }
    else:
        response = {
            'valid': 2
        }
    
    return response