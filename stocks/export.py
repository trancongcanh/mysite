from django.http import HttpResponse
from .models import Company
import csv
from django.shortcuts import redirect
from .common import change_format_date_update
from datetime import datetime, timedelta
from django.conf import settings
# import pandas as pd
# from django.shortcuts import redirect


# Xử lí export file csv
def export_csv(request):
    # Kiểm tra session time out        
    if request.session.get('last_touch',"") != "" :
        # Logout nếu quá session
        if datetime.now() - request.session['last_touch']> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
            member_id = request.session.get('member_id',"")
            del request.session['last_touch']
            if member_id != "":
                del request.session['member_id']
        # Nếu chưa quá session thì thực hiện reset lại session
        else:
            request.session['last_touch'] = datetime.now()
    # Logout nếu quá session
    else:
        member_id = request.session.get('member_id',"")
        if member_id != "":
            del request.session['member_id']
    # Get điều kiện tìm kiếm từ session nếu có để thực hiện export data tương ứng
    company_value = request.session.get("company_value", "")
    count_company = request.session.get('count_company', "")
    date_update = request.session.get('date_update', "")
    # Khởi tạo danh sách công ty
    company_list_db = []
    company_list = []
    # Thay đổi format date lấy từ form để thực hiện get data từ Db
    date_update_change_format = change_format_date_update(date_update)
    # Xử lí các trường hợp với các điều kiện tìm kiếm tương ứng có hoặc không có ngày tìm kiếm, số record
    if (date_update != "" and count_company !=""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        count_record = int(count_company)
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('magic_formula')[:count_record]
    elif (date_update != "" and count_company ==""):
        date_update_view = datetime.strptime(date_update_change_format, "%Y-%m-%d")
        company_list_db = Company.objects.filter(date_update=date_update_view).order_by('magic_formula')
    elif (date_update == "" and count_company !=""):
        count_record = int(count_company)
        company_list_db = Company.objects.all().order_by('magic_formula')[:count_record]
    elif (date_update == "" and count_company ==""):
        company_list_db = Company.objects.all().order_by('magic_formula')

    # Tìm kiếm với công ty có số vốn lớn hơn vốn công ty(nếu có) lấy được từ request 
    if (company_value != ""):
        company_value_validate = int(company_value) 
        for company in company_list_db :
            if (int(company.company_value) >= company_value_validate):
                company_list.append(company)
    else:
        company_list = company_list_db

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'
    # list_stock = []
    # list_magic_formula = []
    # for company in company_list:
    #     list_stock.append(company.stocks)
    #     list_magic_formula.append(company.magic_formula)
    # data = {
    #         'stocks': list_stock, 
            # 'current_price',
            # 'book_value',
            # 'lowest_price_in_52w',
            # 'difference',	
            # 'masses_in_circulation', 
            # 'company_value', 
            # 'e_s_p', 
            # 'r_o_a', 
            # 'r_o_e', 
            # 'p_or_e', 
            # 'p_or_b', 
            # 'is_big_enough', 
            # 'is_lowest', 
    #         'magic_formula': list_magic_formula
    # }

    writer = csv.writer(response)
    writer.writerow(['stocks', 'current_price','book_value','lowest_price_in_52w','difference',	'masses_in_circulation', 'company_value', 'e_s_p', 'r_o_a', 'r_o_e', 'p_or_e', 'p_or_b', 'is_big_enough', 'is_lowest', 'magic_formula'])
    for company in company_list:
        writer.writerow([company.stocks, company.current_price, company.book_value, company.lowest_price_in_52w, company.difference, company.masses_in_circulation, company.company_value, company.e_s_p, company.r_o_a, company.r_o_e, company.p_or_e, company.p_or_b, company.is_big_enough, company.is_lowest, company.magic_formula])
    # df = pd.DataFrame(data, columns= [  'stocks', 
                                                # 'current_price',
                                                # 'book_value',
                                                # 'lowest_price_in_52w',
                                                # 'difference',	
                                                # 'masses_in_circulation', 
                                                # 'company_value', 
                                                # 'e_s_p', 
                                                # 'r_o_a', 
                                                # 'r_o_e', 
                                                # 'p_or_e', 
                                                # 'p_or_b', 
                                                # 'is_big_enough', 
                                                # 'is_lowest', 
                                                # 'magic_formula'])
    # df.to_csv (r'C:/Users/trancongcanh/Downloads/InvestInVn_.csv', index = True, header=True)
    return response
