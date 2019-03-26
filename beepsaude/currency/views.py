from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
import datetime
import requests
import json

# Create your views here.
class Index(View):
    def get(self, request):
        tseries = [self.currencyrequest()]
        dates = []
        for i in range(7):
            myday = datetime.date.today() - datetime.timedelta(days=i)
            myday = myday.strftime("%d/%m/%Y")
            dates.append(myday)
        tseries.append(dates)
        tseries = json.dumps(tseries)
        tseries = json.loads(tseries)
        return JsonResponse(tseries, safe=False)
    
    def currencyrequest(self):
        api_key = 'Your Api Key here!!!'
        url = 'http://apilayer.net/api/historical?access_key={}&date={}&currencies=BRL,EUR,ARS&format=1'
        
        usddata = []
        eurdata = []
        arsdata = []
        for i in range(7):
            date = datetime.date.today() - datetime.timedelta(days=i)
            response = requests.get(url.format(api_key,date))
            response = response.json()
            usd = 1/response['quotes']['USDBRL']
            usddata.append(usd)
            eur = response['quotes']['USDEUR'] * usd
            eurdata.append(eur)
            ars = response['quotes']['USDARS'] * usd
            arsdata.append(ars)
        apiresponse = [{'name':'USD', 'data':usddata}, {'name':'EUR', 'data':eurdata}, {'name':'ARS', 'data':arsdata}]
        return apiresponse

class MyView(View):
    def get(self, request):
        template = loader.get_template('currency/index.html')
        context = {}
        return HttpResponse(template.render(context, request))

    