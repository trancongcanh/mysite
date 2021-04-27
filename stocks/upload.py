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
        if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
            member_id = request.session.get('member_id',"")
            last_touch = request.session.get('last_touch',"")
            if member_id != "" and last_touch != "":
                del request.session['member_id']
                del request.session['last_touch']
            return render(request, 'stocks/login_user.html', {})
        else:
            request.session['last_touch'] = datetime.now()        
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
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
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
