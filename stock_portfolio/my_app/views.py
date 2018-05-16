from django.shortcuts import render
from __future__ import unicode_literals
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

def index_view:
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def details_view: