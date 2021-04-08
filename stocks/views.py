from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse


from .models import Company
 
def index(request):
    try:
        latest_company_list = Company.objects.all()
        template = loader.get_template('stocks/index.html')
        context = {
            'latest_company_list': latest_company_list,
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    return HttpResponse(template.render(context, request))

def search(request):
    try:
        company_capital = request.POST['company_cap']
        count = request.POST['count']
        if (company_capital != ""):
            if (count !=""):
                count_record = int(count)
                latest_company_list = Company.objects.filter(company_cap=company_capital)[:count_record]
            else:
                latest_company_list = Company.objects.filter(company_cap=company_capital)
        else:
            if (count !=""):
                count_record = int(count)
                latest_company_list = Company.objects.all()[:count_record]
            else:
                latest_company_list = Company.objects.all()
        template = loader.get_template('stocks/index.html')
        context = {
            'latest_company_list': latest_company_list,
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    except ValueError:
        latest_company_list=[]
        template = loader.get_template('stocks/index.html')
        context = {
            'latest_company_list': latest_company_list,
        }
    return HttpResponse(template.render(context, request))
