import pymysql
import csv
import configparser
# import mysql.connector

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mysql_config","hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
database = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

conn = pymysql.connect(host=hostname
      , user=username
      , password=password
      , database=database 
      , port=int(port)
)

if conn is None:
    print("Error connecting to the MySQL database")
else:
    print("MySQL Connection Established!")


m_query = "SELECT * FROM family"
local_filename = "family_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter = '|')
    csv_w.writerows(results)
    fp.close()
    m_cursor.close()
    conn.close()