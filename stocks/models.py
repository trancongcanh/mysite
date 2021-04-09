from django.db import models

class Company(models.Model):
    stocks = models.CharField(max_length=10)
    company_name = models.CharField(max_length=70)
    company_cap = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    r_o_a = models.IntegerField(default=0)
    p_e = models.IntegerField(default=0)
    efficiency_level = models.IntegerField(default=0)
    date_update = models.DateField(null=True, blank=True)
    # def __str__(self):
    #     return self.company_name
