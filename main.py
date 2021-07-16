import mysql.connector 
from tqdm import tqdm
import etherscan as scan
from web3 import Web3
import time 
import db
import env

infura_api = env.infura_api
w3 = Web3(Web3.HTTPProvider(infura_api))

apix = env.apix
urlx = env.urlx

pool_addr = env.pool_addr

HOST = env.HOST
USER = env.USER
PASS = env.PASS
db_name = env.db_name

block_one = env.block_one
delay = env.delay

step = env.step

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASS,
    database=db_name
)

def get_recent_block():
    end = scan.GetBlockBeforeTime(time.time(), urlx, apix) 
    end = int(end['result']) # most recent block
    return end

def extract_txs_normal(begin, end):
    from_ = begin 
    to_ = end

    total_blocks = end - begin 
    loop = total_blocks // step
    loop += 1

    for _ in tqdm( range(0,loop) ):
        print(f"extracting normal tx block: {from_} - {to_}")
        txs = scan.GetTransactionsByBlock(pool_addr, apix, urlx, from_, to_)      
        if txs['result'] is not None:
            scan.injectNormalDB(mydb, 'normal_tx', txs['result'])
        
        from_ = to_ + 1
        to_ += step

def populate_normal():
    begin = block_one
    end = get_recent_block()

    extract_txs_normal(begin, end)

def update_normal():
    begin = db.prevBlockNo(mydb, 'normal_tx') 
    begin += 1
    end = get_recent_block()

    extract_txs_normal(begin, end)

def extract_txs_erc20(begin, end):
    from_ = begin 
    to_ = end

    total_blocks = end - begin 
    loop = total_blocks // step
    loop += 1

    for _ in tqdm( range(0,loop) ):
        print(f"extracting erc tx block: {from_} - {to_}")
        txs = scan.GetTransactionsByBlockERC(pool_addr, apix, urlx, from_, to_)  
        if txs['result'] is not None:
            scan.injectErcDB(mydb, 'erc20_tx', txs['result'])
            from_ = to_ + 1
            to_ += step

def populate_erc():
    begin = block_one
    end = get_recent_block()

    extract_txs_erc20(begin, end)

def update_erc():
    begin = db.prevBlockNo(mydb, 'erc20_tx') 
    begin += 1
    end = get_recent_block()

    extract_txs_erc20(begin, end)

def main():
    # NORMAL WORKER
    normal_count = db.countRow(mydb, 'normal_tx')
    if normal_count==0:
        populate_normal()
    elif normal_count>0:
        update_normal()

    # ERC20 WORKER
    erc_count = db.countRow(mydb, 'erc20_tx')
    if erc_count==0:
        populate_erc()
    elif erc_count>0:
        update_erc()  

    mydb.close()

if __name__ == "__main__":
    #while True:
    main()
    #    time.sleep(delay)
