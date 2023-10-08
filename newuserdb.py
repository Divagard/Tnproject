import mysql.connector
db = 'btsuserlogin'
mydb = mysql.connector.connect(host="localhost",user = "root",password = "",database = 'btsuserlogin')
cur = mydb.cursor()
