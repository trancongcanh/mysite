from django.http import HttpResponse, Http404
from django.template import loader
from .models import Company

from .company_view import CompanyView

# Xử lí log out
def logout(request):
    try:
        # Xóa thông tin user khỏi session
        if request.session.get('member_id','') != "":
            del request.session['member_id']
        # Lấy ra data từ CSDL để hiển thị ở MH danh sách
        company_list_db = Company.objects.order_by('-magic_formula')
        # Lấy template để hiển thị sau khi logout
        template = loader.get_template('stocks/index.html')
        # Tạo danh sách đối tượng company mới có thuộc tính index để hiển thị STT table
        company_list_view = []
        for company in company_list_db:
            company_view = CompanyView(0, company.stocks, company.current_price, company.p_or_e, company.company_value, company.r_o_a, company.magic_formula, company.date_update)
            company_list_view.append(company_view)
        for index in range(len(company_list_view)):
            company_list_view[index].id=index+1
        context = {}
        context = {
            'username': "",
            'company_list_view': company_list_view,
        }  
    except Company.DoesNotExist:
        raise Http404('Company does not exist')
    except KeyError:
        pass
    return HttpResponse(template.render(context, request))  