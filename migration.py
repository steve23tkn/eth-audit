import mysql.connector 
import env

HOST = env.HOST
USER = env.USER
PASS = env.PASS

db_name = env.db_name

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASS
)

# CREATE DB
mycursor = mydb.cursor()
mycursor.execute(f"select if( exists(select schema_name from information_schema.schemata where schema_name='{db_name}') , 'True', 'False')")
for x in mycursor:
    if x[0]=='False':
        mycursor.execute(f"create database {db_name}")
mycursor.close()
mydb.close()

# CREATE TABLE - normal_tx
mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASS,
    database=db_name
)

mycursor = mydb.cursor()
create_tx_normal = "create table if not exists normal_tx (id int primary key auto_increment, \
                    blockNumber bigint unsigned, timeStamp bigint unsigned, hash varchar(250), nonce int unsigned, \
                    blockHash varchar(250), transactionIndex bigint unsigned, `from` varchar(100), `to` varchar(100), \
                    value varchar(250), gas varchar(250), gasPrice varchar(250),  \
                    isError int, txreceipt_status int, input varchar(250), \
                    contractAddress varchar(250), cumulativeGasUsed varchar(250), \
                    gasUsed varchar(250), confirmations bigint unsigned)"
mycursor.execute(create_tx_normal)
mycursor.close()

# CREATE TABLE - erc20_tx
mycursor = mydb.cursor()
create_tx_erc20 = "create table if not exists erc20_tx (id int primary key auto_increment, \
                  blockNumber int(50), timeStamp int(50), hash varchar(250), nonce int(10), \
                  blockHash varchar(250), `from` varchar(100), contractAddress varchar(250), \
                  `to` varchar(100), value varchar(250), tokenName varchar(50), \
                  tokenSymbol varchar(10), tokenDecimal int(10), transactionIndex bigint, \
                  gas varchar(250), gasPrice varchar(250), gasUsed varchar(250), \
                  cumulativeGasUsed varchar(50), input varchar(250), confirmations bigint)"
mycursor.execute(create_tx_erc20)
mycursor.close()