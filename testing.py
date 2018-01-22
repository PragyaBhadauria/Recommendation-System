import MySQLdb as mdb

db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()

print"enter company id"
id = int(input())

sim_company = cursor.execute("select sim_comp_id from similarcompany where comp_id = %s" ,[id])


print sim_company
