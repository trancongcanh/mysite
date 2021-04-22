from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
import io,csv
from django.shortcuts import redirect
import pandas


data = pandas.read_csv('D:\data.csv')
for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    _, created = Company.objects.update_or_create(
        stocks=column[0],
        company_name=column[1],
        company_cap=column[2],
        current_price=column[3],
        r_o_a=column[4],
        p_e=column[5],
        efficiency_level=column[6],
        date_update=datetime.now(),
    )

