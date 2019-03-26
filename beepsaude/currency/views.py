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
        #our chart will need 2 info: data to be plotted and the labels. First we'll populate our JSON response with our data
        tseries = [self.currencyrequest()]
        #the list above will be populated with dates that will be our labels
        dates = []
        for i in range(7):
            myday = datetime.date.today() - datetime.timedelta(days=i)
            myday = myday.strftime("%d/%m/%Y")
            dates.append(myday)
        tseries.append(dates)
        #prepare our response as a JSON
        tseries = json.dumps(tseries)
        tseries = json.loads(tseries)
        return JsonResponse(tseries, safe=False)
    
    #This method will consume currencylayer API end get back BRL (brasilian Real), EUR (Euro) and ARS (Argentine Pesos) based on USD (US Dolar). But as the project needs USD, EUR and ARS based on BRL, this method will calculate this currencies quotations based on BRL. After this, the method will return a list with 3 dicts so we can transform it to a json and then use to plot line chart. 
    def currencyrequest(self):
        # The base of the requets
        api_key = 'Your Api Key here!!!'
        url = 'http://apilayer.net/api/historical?access_key={}&date={}&currencies=BRL,EUR,ARS&format=1'
        
        #here we'll take 3 lists that will be used as data by our chart
        usddata = []
        eurdata = []
        arsdata = []
        for i in range(7):
            #because the API key that I have is a free one, I'll need these lines to take the 7 values needed
            #the line below deals with date to be used in our API request
            date = datetime.date.today() - datetime.timedelta(days=i)
            response = requests.get(url.format(api_key,date))
            #Our response will be easier to deal if it's json
            response = response.json()
            #populate our lists
            usd = 1/response['quotes']['USDBRL']
            usddata.append(usd)
            eur = response['quotes']['USDEUR'] * usd
            eurdata.append(eur)
            ars = response['quotes']['USDARS'] * usd
            arsdata.append(ars)
        #define our response
        apiresponse = [{'name':'USD', 'data':usddata}, {'name':'EUR', 'data':eurdata}, {'name':'ARS', 'data':arsdata}]
        return apiresponse

#Because something got wrong with the django template, we'll be using the first View to send a JSON response to be consumed by the View below. 
class MyView(View):
    def get(self, request):
        template = loader.get_template('currency/index.html')
        context = {}
        return HttpResponse(template.render(context, request))

    