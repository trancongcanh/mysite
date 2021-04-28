from datetime import datetime
# Tạo đối tượng Company để hiển thị lên view
class CompanyView:
    id=0;
    stocks="";
    company_value="";
    current_price=0;
    r_o_a=0;
    p_or_e=0;
    magic_formula=0;
    date_update=datetime.now()
    # Constructor
    def __init__(self, id, stocks, current_price, p_or_e, company_value, r_o_a, magic_formula, date_update):
        self.stocks = stocks;
        self.current_price = current_price;
        self.company_value = company_value;
        self.r_o_a = r_o_a;
        self.p_or_e = p_or_e;
        self.magic_formula = magic_formula;
        self.id = id;
        self.date_update = date_update;