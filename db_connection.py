# pip3 install mysql-connector-python
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('HOST'),
    user='root',
    passwd='root',
    database=os.getenv('DATABASE')
)

print(mydb)

mydb.close()