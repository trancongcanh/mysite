from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company, User
import io,csv
from django.shortcuts import redirect

# Xử lí export file csv
def export_csv(request):
    # Get điều kiện tìm kiếm từ session nếu có để thực hiện export data tương ứng
    company_capital = request.session.get("company_cap", "")
    count_company = request.session.get('count_company', "")
    date_update = request.session.get('date_update', "")
    # Khởi tạo danh sách công ty
    company_list_db = []
    company_list = []
    company_list_view= []
    # Thay đổi format date lấy từ form để thực hiện get data từ Db
    date_update_change_format = change_format_date_update(date_update)
    # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng có hoặc không có ngày tìm kiếm, số record
    if (date_update != "" and count_company !=""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        count_record = int(count_company)
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')[:count_record]
    elif (date_update != "" and count_company ==""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')
    elif (date_update == "" and count_company !=""):
        count_record = int(count_company)
        company_list_db = Company.objects.all().order_by('-efficiency_level')[:count_record]
    elif (date_update == "" and count_company ==""):
        company_list_db = Company.objects.all().order_by('-efficiency_level')

    # Tìm kiếm với công ty có số vốn lớn hơn vốn công ty(nếu có) lấy được từ request 
    if (company_capital != ""):
        company_capital_validate = int(company_capital) 
        for company in company_list_db :
            if (int(company.company_cap) >= company_capital_validate):
                company_list.append(company)
    else:
        company_list = company_list_db

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'

    writer = csv.writer(response)
    writer.writerow(['company_name', 'company_cap'])

    for company in company_list:
        writer.writerow([company.company_name, company.company_cap])

    return response