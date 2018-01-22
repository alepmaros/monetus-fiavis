import json, requests, simplejson
from pprint import pprint

def get_stocks():
    companies = json.load(open('stocks.json'))

    for x in range(0, len(companies['stocks'])):
        companystatus = get_company_status(companies['stocks'][x]['code'])

        if (companystatus !== 100 or companystatus !== 200):
            companies['stocks'][x]['status'] = companystatus

    return (companies)

# retorna 100 se uma ação específica retornou erro
# retorna 200 se houve erro no retorno da API
def get_company_status(company):
    rsp = requests.get('https://finance.google.com/finance?q=' + company + '&output=json')
    
    if (rsp.status_code == 200):
        company_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))

        if ('cp' in company_data):
            return (float(company_data['cp']) / 100)
        else:
            return 100
    else:
        return 200