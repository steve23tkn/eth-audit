import mysql.connector

def retrieveAll(mydb, table):
    mycursor = mydb.cursor()
    sql = f'select * from {table}'
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    #arr = []
    #for item in rows:
        #arr.append(item[1])
        #print(item)
    #return arr
    return rows

def prevBlockNo(mydb, table):
    mycursor = mydb.cursor()
    sql = f'select max(blockNumber) from {table}'
    mycursor.execute(sql)
    row = mycursor.fetchone()

    return row[0] 

def countRow(mydb, table):
    mycursor = mydb.cursor()
    sql = f'select count(id) from {table}'
    mycursor.execute(sql)
    row = mycursor.fetchone()

    return row[0] # int
