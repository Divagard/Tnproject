import mysql.connector
db = "newuserentry"
mydb = mysql.connector.connect(host="localhost",user = "root",password = "",database = "newuserentry")
cur = mydb.cursor()
