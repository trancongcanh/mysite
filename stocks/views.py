from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from datetime import datetime
from .models import Company

# Xử lí hiển thị MH danh sách công ty
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

# Xử lí hiển thị trường hợp search
def search(request):
    try:
        # Get dữ liệu từ request
        company_capital = request.POST['company_cap']
        count_company = request.POST['count_company']
        date_update = request.POST['date_update']
        # Khởi tạo biến và danh sách
        latest_company_list_view = []
        latest_company_list = []
        date_update_view = ""
        # Validate dữ liệu từ request
        if (date_update != ""):
            date_update_view_list = []
            date_update_view_list = date_update.split("/")
            for index in range(len(date_update_view_list)):
                if (index == 0) :
                    date_update_view = str(date_update_view_list[index])
                else:
                    date_update_view = str(date_update_view_list[index]) + "-" + date_update_view
            date_update_view = datetime.strptime(date_update_view, "%Y-%m-%d")
        if (count_company != ""): 
            count_record = int(count_company)
        if (company_capital != ""):
            company_capital_validate = int(company_capital)
        # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng
        if (date_update != "" and company_capital != "" and count_company !=""):
            latest_company_list_view = Company.objects.filter(company_cap=company_capital_validate, date_update=date_update_view).order_by('-efficiency_level')[:count_record]
        elif (date_update != "" and company_capital != "" and count_company ==""):
            latest_company_list_view = Company.objects.filter(company_cap=company_capital, date_update=date_update_view).order_by('-efficiency_level')
        elif (date_update != "" and company_capital == "" and count_company !=""):
            latest_company_list_view = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')[:count_record]
        elif (date_update != "" and company_capital == "" and count_company ==""):
            latest_company_list_view = Company.objects.filter(date_update=date_update_view).order_by('-efficiency_level')
        elif (date_update == "" and company_capital != "" and count_company !=""):
            latest_company_list_view = Company.objects.filter(company_cap=company_capital).order_by('-efficiency_level')[:count_record]
        elif (date_update == "" and company_capital != "" and count_company ==""):
            latest_company_list_view = Company.objects.filter(company_cap=company_capital, date_update=date_update_view).order_by('-efficiency_level')
        elif (date_update == "" and company_capital == "" and count_company !=""):
            latest_company_list_view = Company.objects.all().order_by('-efficiency_level')[:count_record]
        elif (date_update == "" and company_capital == "" and count_company ==""):
            latest_company_list_view = Company.objects.all().order_by('-efficiency_level')
        # Duyệt các chỉ số hiển thị của mỗi record
        for index in range(len(latest_company_list_view)):
            latest_company_list_view[index].id=index+1
        # Lấy ra số lượng thực tế các công ty thỏa mãn điều kiện tìm kiếm
        len_company = len(latest_company_list)
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
            'date_update_view': date_update,
            'len_company': len_company,
            'count_record_view': count_company,
            'company_capital_view': company_capital,
            'latest_company_list': latest_company_list_view,
        }
    except (KeyError, Company.DoesNotExist):
        raise Http404('Company does not exist')
    # Xử lí validate dữ liệu tìm kiếm từ form
    except ValueError:
        message = ''
        message2 = ''
        message3 = ''
        # Validate lỗi nhập điều kiện tìm kiếm theo vốn công ty
        if (company_capital != ""):
            try:
                int(company_capital)
            except ValueError:
                message = "Vốn công ty chỉ chứa số half size."
        # Validate khi nhập điều kiện tìm kiếm số công ty muốn hiển thị
        if (count_company !=""):
            try:
                int(count_company)
            except ValueError:
                message2 = "Số record chỉ chứa số half size."
        # Validate khi nhập điều kiện tìm kiếm ngày cập nhật công ty sai định dạng
        if (date_update !=""):
            try:
                date_update_view = ""
                if (date_update != ""):
                    date_update_view_list = []
                    date_update_view_list = date_update.split("/")
                    for index in range(len(date_update_view_list)):
                        if (index == 0) :
                            date_update_view = str(date_update_view_list[index])
                        else:
                            date_update_view = str(date_update_view_list[index]) + "-" + date_update_view
                date_update_view = datetime.strptime(date_update_view, "%Y-%m-%d")
            except ValueError:
                message3 = "Ngày tìm kiếm sai định dạng." 
        # Do điều kiện tìm kiếm sai format nên khởi tạo 1 danh sách rỗng để hiển thị    
        latest_company_list=[]
        # Get ra template theo đường dẫn tương ứng để set hiển thị
        template = loader.get_template('stocks/index.html')
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
                    'date_update_view': date_update,                    
                    'count_record_view': count_company,
                    'company_capital_view': company_capital,
                    'message': message,
                    'message2': message2,
                    'message3': message3,
                    'latest_company_list': latest_company_list,
                }

    # Trả về dữ liệu hiển thị trên tempalte
    return HttpResponse(template.render(context, request))
