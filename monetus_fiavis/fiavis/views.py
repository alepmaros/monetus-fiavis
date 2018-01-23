from django.shortcuts import render
from django.core import serializers

from .models import Stock

def index_fiavis(request):

    stocks = Stock.objects.all()
    stocks_json = serializers.serialize('json', stocks)

    return render(request, 'fiavis/index.html', {'stocks': stocks_json})