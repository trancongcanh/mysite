from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import Company
 
def index(request):
    try:
        latest_company_list = Company.objects.order_by('efficiency_level')
        # latest_companys=latest_company_list
        # latest_company_list_sort = []
        # for company in latest_company_list:
        #     latest_company_list_sort.append(company.efficiency_level)
        # latest_company_list_sort_laster = latest_company_list_sort.sort()
        # for company in latest_company_list:
        #     for company in latest_company_list:
        #         if (latest_company_list_sort_laster != []) :
        #             if (company.efficiency_level == latest_company_list_sort_laster[0]):
        #                 latest_companys.append(company)
        #                 del latest_company_list_sort_laster[0]
            
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
        company_capital_view=''
        count_record_view=''
        if (company_capital != ""):
            company_capital_view=company_capital
            if (count !=""):
                count_record_view=count
                count_record = int(count)
                latest_company_list = Company.objects.filter(company_cap=company_capital)[:count_record]
            else:
                latest_company_list = Company.objects.filter(company_cap=company_capital)
        else:
            if (count !=""):
                count_record = int(count)
                count_record_view=count
                latest_company_list = Company.objects.all()[:count_record]
            else:
                latest_company_list = Company.objects.all()
        template = loader.get_template('stocks/index.html')
        context = {
            'count_record_view': count_record_view,
            'company_capital_view': company_capital,
            'latest_company_list': latest_company_list,
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    except ValueError:
        message = ''
        message2 = ''
        if (company_capital != ""):
            company_capital_view = company_capital
            try:
                company_capital_view = int(company_capital)
            except ValueError:
                message = "Vốn công ty chỉ chứa số half size."
        if (count !=""):
            count_record_view = count  
            try:
                count_record = int(count)
            except ValueError:
                message2 = "Số record chỉ chứa số half size."
        latest_company_list=[]
        template = loader.get_template('stocks/index.html')
        context = {
                    'count_record_view': count_record_view,
                    'company_capital_view': company_capital,
                    'message': message,
                    'message2': message2,
                    'latest_company_list': latest_company_list,
                }
    return HttpResponse(template.render(context, request))
