from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime
from pytz import timezone
from django.shortcuts import render
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd



# Create your views here.
@csrf_exempt
def index_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def getStockDetails(symbol):
    url = "https://www.alphavantage.co/query?apikey=JVBIA4MVP0BBMTIN&function=TIME_SERIES_WEEKLY_ADJUSTED&symbol="+symbol
    response = requests.get(url)
    body = response.json()

    d = body['Weekly Adjusted Time Series']
    data = []
    n=0

    headers = {"Accept":"application/json", "Authorization":"Bearer JIhRpxG1YcwcUZlK6hR5wtsEAvjI"}
    name_url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol
    name_response = requests.get(name_url, headers=headers)
    name = name_response.json()['quotes']['quote']['description']
    
    keys = []
    values = []

    for k,v in d.items():
        temp = json.dumps(v)
        data.append(temp)
        keys.append(k)
        values.append(json.loads(temp)['4. close'])
        n = n+1
        if n>31:
            break

    today = json.loads(data[0])
    yesterday = json.loads(data[1])

    today_close = today['4. close']
    yesterday_close = yesterday['4. close']
    change =  float(today_close) - float(yesterday_close)
    today_open = today['1. open']
    today_high = today['2. high']
    today_low = today['3. low']

    change_percentage = change/float(yesterday_close)

    color = '#000000'

    if change > 0:
        color = '#4CAF50'
    else:
        color = '#F44336'
    
    if change > 0:
        temp = "+"
    else:
        temp = ""

    change_percentage *= 100

    details = {
        'symbol':symbol,
        'name' : name,
        'open' : f"{float(today_open):.2f}",
        'close' : f"{float(today_close):.2f}",
        'high' : f"{float(today_high):.2f}",
        'low' : f"{float(today_low):.2f}",
        'change_percentage' : temp + str(f"{float(change_percentage):.4f}"),
        'currency' : 'USD',
        'change' : temp + str(f"{change:.4f}"),
        'color' : color,
        'prev_close' : f"{float(yesterday_close):.2f}",
        'keys':keys,
        'values':values
    }

    return details

@csrf_exempt
def details_view(request):
    if request.method == 'POST':
        
        amount = request.POST.get('amount')
        
        is_ethical_enabled = request.POST.get('ethical_investing')
        is_growth_enabled = request.POST.get('growth_investing')
        is_index_enabled = request.POST.get('index_investing')
        is_quality_enabled = request.POST.get('quality_investing')
        is_value_enabled = request.POST.get('value_investing')
        
        companies_json = '{"strategies":{"Ethical Investing":[{"name":"AAPL","portion":"30"},{"name":"ADBE","portion":"15"},{"name":"NKE","portion":"25"},{"name":"JCI","portion":"30"}],"Growth Investing":[{"name":"EBAY","portion":"25"},{"name":"MSFT","portion":"35"},{"name":"INTC","portion":"25"},{"name":"AMZN","portion":"15"}],"Index Investing":[{"name":"IBM","portion":"25"},{"name":"TWTR","portion":"35"},{"name":"CDNS","portion":"25"},{"name":"SNPS","portion":"15"}],"Quality Investing":[{"name":"FB","portion":"15"},{"name":"WMT","portion":"45"},{"name":"CRM","portion":"15"},{"name":"QDF","portion":"25"}],"Value Investing":[{"name":"TSLA","portion":"15"},{"name":"PYPL","portion":"25"},{"name":"FDX","portion":"40"},{"name":"STX","portion":"20"}]}}'

        companies = json.loads(companies_json)

        stock_symbols = []
        stock_weights = []
        count = 0
        types = []
        if is_ethical_enabled == 'Ethical Investing':
            count += 1
            types.append(is_ethical_enabled)
            ethical_companies = companies['strategies']['Ethical Investing']
            for ethical_company in ethical_companies:
                stock_symbols.append(ethical_company['name'])
                stock_weights.append(ethical_company['portion'])
        
        if is_growth_enabled == 'Growth Investing':
            count += 1
            types.append(is_growth_enabled)
            ethical_companies = companies['strategies']['Growth Investing']
            for ethical_company in ethical_companies:
                stock_symbols.append(ethical_company['name'])
                stock_weights.append(ethical_company['portion'])

        if is_index_enabled == 'Index Investing':
            count += 1
            types.append(is_index_enabled)
            ethical_companies = companies['strategies']['Index Investing']
            for ethical_company in ethical_companies:
                stock_symbols.append(ethical_company['name'])
                stock_weights.append(ethical_company['portion'])

        if is_quality_enabled == 'Quality Investing':
            count += 1
            types.append(is_quality_enabled)
            ethical_companies = companies['strategies']['Quality Investing']
            for ethical_company in ethical_companies:
                stock_symbols.append(ethical_company['name'])
                stock_weights.append(ethical_company['portion'])

        if is_value_enabled == 'Value Investing':
            count += 1
            types.append(is_value_enabled)
            ethical_companies = companies['strategies']['Value Investing']
            for ethical_company in ethical_companies:
                stock_symbols.append(ethical_company['name'])
                stock_weights.append(ethical_company['portion'])

        total = float(amount)

        stock_values = []
        for stock_weight in stock_weights:
            temp = float(total)*float(stock_weight)/100
            stock_values.append(temp/count)

        stock_details = []

        for stock_symbol in stock_symbols:
            stock_details.append(getStockDetails(stock_symbol))

        stock_names = []
        stock_closings = []
        stock_divs = []

        for stock_detail in stock_details:
            stock_divs.append(get_plot(stock_detail['keys'], stock_detail['values'],stock_detail['name']))
            stock_names.append(stock_detail['name'])
            stock_closings.append(stock_detail['close'])

        many_selection = True if count > 1 else False

        if many_selection == False:
            
            whole_data = zip(stock_names,stock_closings,stock_symbols,stock_values)
            context = {
                "many_selection" : many_selection,
                "whole_data" : whole_data,
                "types" : types,
                "graphs" : stock_divs
            }
            
        else:
            names_1 = stock_names[0:4]
            names_2 = stock_names[4:8]

            closings_1 = stock_closings[0:4]
            closings_2 = stock_closings[4:8]

            symbols_1 = stock_symbols[0:4]
            symbols_2 = stock_symbols[4:8]

            values_1 = stock_values[0:4]
            values_2 = stock_values[4:8]

            whole_data_1 = zip(names_1,closings_1,symbols_1,values_1)
            whole_data_2 = zip(names_2,closings_2,symbols_2,values_2)

            context = {
                "many_selection" : many_selection,
                "whole_data_1" : whole_data_1,
                "whole_data_2" : whole_data_2,
                "types" : types,
                "graphs" : stock_divs
            }
        print(context)
        return render(request, "details.html", context)

def get_plot(x_val,y_val,name):
    trace1 = go.Scatter(x=x_val,y=y_val)
    data=go.Data([trace1])
    layout=go.Layout(title="Week data of "+name, xaxis={'title':'Date'}, yaxis={'title':'Closing Value'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')
    return div
