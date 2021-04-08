from sqlalchemy import *
from config import host, port, database, user, password
conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()
first_tb = Table('stocks_company', metadata,
    Column('stocks', String(10), nullable=False),
    Column('company_name', String(70), nullable=False),
    Column('company_cap', int(), nullable=False),
    Column('current_price', int(), nullable=False),
    Column('r_o_a', int(), nullable=False),
    Column('p_e', int(), nullable=False),
    Column('efficiency_level', int(), nullable=False),
)
metadata.create_all(engine)
query = insert(first_tb).values(id=1, name="Company", isHappy=True)
ResultProxy = connection.execute(query)