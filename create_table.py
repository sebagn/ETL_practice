from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

#load variables
dotenv.load_dotenv()
user = os.getenv("user")
password = os.getenv("password")
host="data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
port=5439
database='data-engineer-database'

Base = declarative_base()
class YourTable(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    symbol = Column(String)
    change = Column(Float)
    change_percent = Column(Float)
    
engine = create_engine(f'redshift+psycopg2://{user}:{password}@{host}:{port}/{database}')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()