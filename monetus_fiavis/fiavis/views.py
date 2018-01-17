from django.shortcuts import render

def index_fiavis(request):
    return render(request, 'fiavis/index.html', {'variavel': 'abc'})