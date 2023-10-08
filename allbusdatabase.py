import mysql.connector
dbname = 'allbusinformation'
db = "newemreg"
db1 = 'busreg'
db2 = 'busreason'
db3 = 'busalot'
mydb = mysql.connector.connect(host="localhost",user = "root",password = "",database = "allbusinformation")
cur = mydb.cursor()
