from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Company, User
import io,csv
from django.shortcuts import redirect
from django.conf import settings

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
        # Lấy mẫu template
        template = 'stocks/profile_upload.html'
        data = Company.objects.all()
        # Tạo 1 Dictionary đưa lên template hiển thị 
        prompt = {
            'profiles': data    
        }
        # Xử lí hiển thị ban đầu khi vào trang upload file
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES.get('profile_upload', "")
        if csv_file == "":
            context = {
                'messages': "Chưa chọn file upload"
            }
            # Trả về template hiển thị sau khi upload file thất bại
            return render(request, template, context)
        # Kiểm tra xem tệp đầu vào phải là tệp csv không
        if not csv_file.name.endswith('.csv'):
            context = {
                'messages': "File upload không phải tệp csv"
            }
            # Trả về template hiển thị sau khi upload file thất bại
            return render(request, template, context)
        data_set = csv_file.read().decode('utf-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        id = 9
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Company.objects.update_or_create(
                stocks=column[0],
                current_price=column[1],
                book_value=column[2],
                lowest_price_in_52w=column[3],
                difference=column[4],
                masses_in_circulation=float(column[5]),
                company_value=float(column[6]),
                e_s_p=column[7],
                r_o_a=column[8],
                r_o_e=column[9],
                p_or_e=column[10],
                p_or_b=column[11],
                is_big_enough=converStringtoBoolean(column[12]),
                is_lowest=converStringtoBoolean(column[13]),
                magic_formula=column[14],
                date_update=datetime.now(),
            )
            
        # Tạo 1 Dictionary đưa lên template hiển thị 
        context = {
        'messages': "Upload file thành công"
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

# Chuyển đổi giá trị True/False từ các cộgt trong csv thành giá trị Boolean mà ứng dụng hiểu được khi thêm vào DB
def converStringtoBoolean (string) :
    check_bolean = True
    for i in range(len(string)):
        if string[i] == 'F' or string[i] =='f':
            check_bolean = False
    return check_bolean

