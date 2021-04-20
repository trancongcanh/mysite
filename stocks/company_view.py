from datetime import datetime
# Tạo đối tượng Company để hiển thị lên view
class CompanyView:
    id=0;
    stocks="";
    company_name="";
    company_cap=0;
    current_price=0;
    r_o_a=0;
    p_e=0;
    efficiency_level=0;
    date_update=datetime.now()
    # Constructor
    def __init__(self, id, stocks, company_name, company_cap, current_price, r_o_a, p_e, efficiency_level, date_update):
        self.stocks = stocks;
        self.company_name = company_name;
        self.company_cap = company_cap;
        self.current_price = current_price;
        self.r_o_a = r_o_a;
        self.p_e = p_e;
        self.efficiency_level = efficiency_level;
        self.date_update = date_update;
        self.id = id;