from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://admin:blacklist1234@blacklistdb.c97kwizh5fyb.us-east-1.rds.amazonaws.com:3306/blacklistdb"

metadata = MetaData()
engine = create_engine(DATABASE_URL)
metadata.create_all(engine, checkfirst=True)

database = Database(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(100))
    name = Column(String(50))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
