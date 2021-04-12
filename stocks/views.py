from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from datetime import datetime


from .models import Company
 
def index(request):
    try:
        latest_company_list_view = Company.objects.order_by('efficiency_level')
        latest_company_list = latest_company_list_view.reverse()    
        template = loader.get_template('stocks/index.html')
        for index in range(len(latest_company_list)):
            latest_company_list[index].id=index+1
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
        date_update = request.POST['date_update']
        company_capital_view=''
        count_record_view=''
        latest_company_list_view = []
        latest_company_list = []
        date_update_view = ""
        date_update_view_list = date_update.split("/")
        date_update_view = date_update_view_list[2] + "-" + date_update_view_list[1] + "-" + date_update_view_list[0]
        date_update_view = datetime.strptime(date_update_view, "%Y-%m-%d")
        if (date_update != ""):
            if (company_capital != ""):
                company_capital_view=company_capital
                if (count !=""):
                    count_record_view=count
                    count_record = int(count)
                    latest_company_list_view = Company.objects.filter(company_cap=company_capital, date_update=date_update_view).order_by('efficiency_level')[:count_record]
                else:
                    latest_company_list_view = Company.objects.filter(company_cap=company_capital, date_update=date_update_view).order_by('efficiency_level')
            else:
                if (count !=""):
                    count_record = int(count)
                    count_record_view=count
                    latest_company_list_view = Company.objects.filter(date_update=date_update_view).order_by('efficiency_level')[:count_record]
                else:
                    latest_company_list_view = Company.objects.filter(date_update=date_update_view).order_by('efficiency_level')
        else:
            if (company_capital != ""):
                company_capital_view=company_capital
                if (count !=""):
                    count_record_view=count
                    count_record = int(count)
                    latest_company_list_view = Company.objects.filter(company_cap=company_capital).order_by('efficiency_level')[:count_record]
                else:
                    latest_company_list_view = Company.objects.filter(company_cap=company_capital).order_by('efficiency_level')
            else:
                if (count !=""):
                    count_record = int(count)
                    count_record_view=count
                    latest_company_list_view = Company.objects.all().order_by('efficiency_level')[:count_record]
                else:
                    latest_company_list_view = Company.objects.all().order_by('efficiency_level')

        list_tmp = []
        for company in latest_company_list_view:
            list_tmp = [company]
            latest_company_list = list_tmp + latest_company_list
        for index in range(len(latest_company_list)):
            latest_company_list[index].id=index+1
        len_company = len(latest_company_list)
        template = loader.get_template('stocks/index.html')
        context = {
            'date_update_view': date_update,
            'len_company': len_company,
            'count_record_view': count_record_view,
            'company_capital_view': company_capital,
            'latest_company_list': latest_company_list,
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    except ValueError:
        message = ''
        message2 = ''
        message3 = ''
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
        if (date_update !=""):
            try:
                date_update_view = ""
                date_update_view_list = date_update.split("/")
                date_update_view = date_update_view_list[2] + "-" + date_update_view_list[1] + "-" + date_update_view_list[0]
                date_update_view = datetime.strptime(date_update_view, "%Y-%m-%d")
            except ValueError:
                message3 = "Ngày tìm kiếm sai định dạng."        
        latest_company_list=[]
        template = loader.get_template('stocks/index.html')
        context = {
                    'date_update_view': date_update,                    
                    'count_record_view': count_record_view,
                    'company_capital_view': company_capital,
                    'message': message,
                    'message2': message2,
                    'message3': message3,
                    'latest_company_list': latest_company_list,
                }
    return HttpResponse(template.render(context, request))
