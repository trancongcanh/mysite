from django.db import models
#Tạo bảng các công ty và các thuộc tính tương ứng
class Company(models.Model):
    # Mã cổ phiếu	
    stocks = models.CharField(max_length=10)
    # Tên công  ty
    company_name = models.CharField(max_length=70)
    # Vốn công ty
    company_cap = models.IntegerField(default=0)
    # Giá hiện tại
    current_price = models.IntegerField(default=0)
    # ROA (%)
    r_o_a = models.IntegerField(default=0)
    # PE
    p_e = models.IntegerField(default=0)
    # Mức độ hiệu quả
    efficiency_level = models.IntegerField(default=0)
    # Ngày cập nhật
    date_update = models.DateField(null=True, blank=True)

