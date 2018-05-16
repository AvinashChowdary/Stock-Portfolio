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

# Create your views here.
@csrf_exempt
def index_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
@csrf_exempt
def details_view(request):
    if request.method == 'POST':
        
        amount = request.POST.get('amount')
        
        is_ethical_enabled = request.POST.get('ethical_investing')
        is_growth_enabled = request.POST.get('griowth_investing')
        is_index_enabled = request.POST.get('index_investing')
        is_quality_enabled = request.POST.get('quality_investing')
        is_value_enabled = request.POST.get('value_investing')
        
        context = {
            "amount" : amount,
            "is_ethical_enabled" : is_ethical_enabled,
            "is_growth_enabled" : is_growth_enabled,
            "is_index_enabled" : is_index_enabled,
            "is_quality_enabled" : is_quality_enabled,
            "is_value_enabled" : is_value_enabled
        }
        
        
        return render(request, "details.html", context)