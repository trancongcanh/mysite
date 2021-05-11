from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User
import io,csv
from django.shortcuts import redirect
from django.conf import settings
import pandas as pd
from .common import converToInt

# Xử lí upload file
def profile_upload(request):
    try:
        # Kiểm tra session time out        
        if request.session.get('last_touch',"") != "" :
            # Logout và Quay lại MH login nếu quá session
            if datetime.now() - request.session['last_touch']> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                member_id = request.session.get('member_id',"")
                del request.session['last_touch']
                if member_id != "":
                    del request.session['member_id']
                    return redirect("stocks:login")
            # Nếu chưa quá session thì thực hiện reset lại session
            else:
                request.session['last_touch'] = datetime.now()
        # Logout và Quay lại MH login nếu quá session
        else:
            member_id = request.session.get('member_id',"")
            if member_id != "":
                del request.session['member_id']
                return redirect("stocks:login")  
        # Lấy mẫu template hiển thị
        template = 'stocks/profile_upload.html'
        # Tạo 1 Dictionary đưa lên template hiển thị 
        # prompt = {
        # }
        # # Xử lí hiển thị ban đầu khi vào trang upload file
        # if request.method == "GET":
        #     return render(request, template, prompt) 
        # csv_file = request.FILES.get('profile_upload', "")
        # if csv_file == "":
        #     context = {
        #         'messages': "Chưa chọn file upload"
        #     }
        #     # Trả về template hiển thị sau khi upload file thất bại
        #     return render(request, template, context)
        # Kiểm tra xem tệp đầu vào phải là tệp csv không
        # if not csv_file.name.endswith('.csv'):
        #     context = {
        #         'messages': "File upload không phải tệp csv"
        #     }
        #     # Trả về template hiển thị sau khi upload file thất bại
        #     return render(request, template, context)
        # data_set = csv_file.read().decode('utf-8')
        # # setup a stream which is when we loop through each line we are able to handle a data in a stream
        # io_string = io.StringIO(data_set)
        # next(io_string)
        data = pd.read_csv (r'C:/Users/trancongcanh/Downloads/InvestInVn_.csv')
        df = pd.DataFrame(data, columns= [
            'Ma CP',
            'Current Price',
            'Book Value', 
            'Lowest Price In 52w', 
            'Chenh lech', 
            'KL dang luu hanh', 
            'Gia tri cong ty',
            'EPS',
            'ROA',
            'ROE',
            'P/E',
            'P/B',
            'Is Big Enough',
            'IsLowest',
            'MagicFormula',
        ])
        company_list = df.values.tolist()
        for column in company_list:
            created = Company.objects.create(
                stocks=column[0],
                current_price=column[1],
                book_value=column[2],
                lowest_price_in_52w=column[3],
                difference=column[4],
                masses_in_circulation=converToInt(column[5]),
                company_value=converToInt(column[6]),
                e_s_p=column[7],
                r_o_a=column[8],
                r_o_e=column[9],
                p_or_e=column[10],
                p_or_b=column[11],
                is_big_enough=column[12],
                is_lowest=column[13],
                magic_formula=column[14],
                date_update=datetime.now(),
            )
            
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
        'messages': "Upload file thành công",
        'df': df
        }
        # Trả về template hiển thị sau khi upload file thành công
        return render(request, template, context)
    except Exception:
        # Lấy mẫu template
        template = 'stocks/profile_upload.html'        
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
            'messages': "Upload file không thành công, vui lòng kiểm tra lại file upload và thử lại"
        }
        # Trả về template hiển thị sau khi upload file thành công
        return render(request, template, context)


