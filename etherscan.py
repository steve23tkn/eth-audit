import requests 
import json 
import time
import csv
from csv import writer

def GetTransactionsByBlock(address, api, url, start, end):
    try:
        payload = {
            'module' : 'account',
            'action' : 'txlist',
            'address' : address,
            'startblock' : str(start),
            'endblock' : str(end),
            'sort' : 'asc',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        return result
    except Exception as e:
        return {'result': None, 'log': e, 'address': address}

def GetTransactionsByBlockERC(address, api, url, start, end):
    try:
        payload = {
            'module' : 'account',
            'action' : 'tokentx',
            'address' : address,
            'startblock' : str(start),
            'endblock' : str(end),
            'sort' : 'asc',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        return result
    except Exception as e:
        return {'result': None, 'log': e, 'address': address} 
    
def GetEtherBalance(address, api, url):
    try:
        payload = {
            'module' : 'account',
            'action' : 'balance',
            'address' : address,
            'tag' : 'latest',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        bal = int(result['result']) / 1000000000000000000
        
        return {'result': bal, 'address': address}
    except Exception as e:
        return {'result': None, 'log': e, 'address': address} 
    
#https://api.etherscan.io/api?module=account&action=tokenbalance&
#    contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&
#    address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&tag=latest&apikey=YourApiKeyToken

def GetErc20Balance(contract, address, api, url):
    try:
        payload = {
            'module' : 'account',
            'action' : 'tokenbalance',
            'contractaddress' : contract,
            'address' : address,
            'tag' : 'latest',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        bal = int(result['result']) 
        
        return {'result': bal, 'address': address}
    except Exception as e:
        return {'result': None, 'log': e, 'address': address} 
    
def GetIdkBalance(address, api, url):
    try:
        payload = {
            'module' : 'account',
            'action' : 'tokenbalance',
            'contractaddress' : '0x61fd1c62551850d0c04c76fce614cbced0094498',
            'address' : address,
            'tag' : 'latest',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        bal = int(result['result']) / 100000000
        
        return {'result': bal, 'address': address}
    except Exception as e:
        return {'result': None, 'log': e, 'address': address} 
    
def InitFile(file_name, list_header):
    csv_file = open(file_name, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list_header) # ['id', 'user_addr']
    csv_file.close()     
    
def InjectListToFile(txes, file_name):
    
    #CHECK IF NONETYPE
    #['blockNumber','timeStamp','hash','nonce','blockHash','from','contractAddress','to','value','tokenName',
 #'tokenSymbol','tokenDecimal','transactionIndex','gas','gasPrice','gasUsed','cumulativeGasUsed','input',
 #'confirmations']
    
    for tx in txes:   
        
        data = []
        data.append(tx['blockNumber'])       
        data.append(tx['timeStamp'])
        data.append(tx['hash'])
        data.append(tx['nonce'])
        data.append(tx['blockHash'])
        data.append(tx['from'])
        data.append(tx['contractAddress'])
        data.append(tx['to'])
        data.append(tx['value'])        
        data.append(tx['tokenName'])
        
        data.append(tx['tokenSymbol'])
        data.append(tx['tokenDecimal'])
        data.append(tx['transactionIndex'])
        data.append(tx['gas'])        
        data.append(tx['gasPrice'])
        data.append(tx['gasUsed'])
        data.append(tx['cumulativeGasUsed'])
        data.append(tx['input'])
        data.append(tx['confirmations'])
        
        with open(file_name, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()  

def injectNormalDB(mydb, table, txs):
    for tx in txs:
        blockNumber_ = tx['blockNumber']

        blockHash_ = tx['blockHash']
        timeStamp_ = tx['timeStamp']
        hash_ = tx['hash']
        nonce_ = tx['nonce']

        transactionIndex_ = tx['transactionIndex']
        from_ = tx['from']
        to_ = tx['to']
        value_ = tx['value']
        gas_ = tx['gas']

        gasPrice_ = tx['gasPrice']
        input_ = tx['input']
        contractAddress_ = tx['contractAddress']
        cumulativeGasUsed_ = tx['cumulativeGasUsed']
        txreceipt_status_ = tx['txreceipt_status']

        gasUsed_ = tx['gasUsed']
        confirmations_ = tx['confirmations']
        isError_ = tx['isError']

        mycursor = mydb.cursor()

        sql = f"insert into {table} (blockNumber, timeStamp, hash, nonce, blockHash, \
                transactionIndex, `from`, `to`, value, gas, gasPrice, isError, \
                txreceipt_status, input, contractAddress, cumulativeGasUsed, \
                gasUsed, confirmations) values ({blockNumber_}, {timeStamp_}, '{hash_}', \
                {nonce_}, '{blockHash_}', \
                {transactionIndex_}, '{from_}', '{to_}', {value_}, {gas_}, {gasPrice_}, {isError_}, \
                {txreceipt_status_}, '{input_}', '{contractAddress_}', {cumulativeGasUsed_}, \
                {gasUsed_}, {confirmations_})"

        mycursor.execute(sql)

        mydb.commit() 

def injectErcDB(mydb, table, txs):
    for tx in txs:
        blockNumber_ = tx['blockNumber']

        blockHash_ = tx['blockHash']
        timeStamp_ = tx['timeStamp']
        hash_ = tx['hash']
        print(f"injecting tx: {hash_}")
        nonce_ = tx['nonce']

        transactionIndex_ = tx['transactionIndex']
        from_ = tx['from']
        to_ = tx['to']
        value_ = tx['value']
        gas_ = tx['gas']

        gasPrice_ = tx['gasPrice']
        input_ = tx['input']
        contractAddress_ = tx['contractAddress']
        cumulativeGasUsed_ = tx['cumulativeGasUsed']

        gasUsed_ = tx['gasUsed']
        confirmations_ = tx['confirmations']

        tokenName_ = tx['tokenName']
        tokenSymbol_ = tx['tokenSymbol']
        tokenDecimal_ = tx['tokenDecimal']

        mycursor = mydb.cursor()

        sql = f"insert into {table} (blockNumber, timeStamp, hash, nonce, \
            blockHash, `from`, contractAddress, \
            `to`, value, tokenName, \
            tokenSymbol, tokenDecimal, transactionIndex, \
            gas, gasPrice, gasUsed, \
            cumulativeGasUsed, input, confirmations) values (\
            {blockNumber_}, {timeStamp_}, \
            '{hash_}', {nonce_},\
            '{blockHash_}', '{from_}', '{contractAddress_}',\
            '{to_}', '{value_}', '{tokenName_}', \
            '{tokenSymbol_}', {tokenDecimal_}, {transactionIndex_}, \
            '{gas_}', '{gasPrice_}', '{gasUsed_}', \
            '{cumulativeGasUsed_}', '{input_}', {confirmations_})"  
                
        mycursor.execute(sql)

        mydb.commit() 

def injectListToDBTest(mydb, table, txs):
    mycursor = mydb.cursor()

    for tx in txs:
        
        hash_ = tx['hash']
        
        sql = f"insert into {table} (hash) values ('{hash_}')"

        mycursor.execute(sql)

    mydb.commit() 
            
def IsTxMatched(tx, df):
    df_result = df[ df['tx']==tx ]
    if len(df_result)>0:
        return True 
    return False

def GetFirstTx(address, api, url):
    try:
        payload = {
            'module' : 'account',
            'action' : 'txlist',
            'address' : address,
            'startblock' : '0',
            'endblock' : '999999999',
            'page' : '10',
            'offset' : '1',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure', 'address': address}
        
        return result
    except Exception as e:
        return {'result': None, 'log': e, 'address': address} 
    
def GetRecentBlock(url, api):
    try:
        payload = {
            'module' : 'block',
            'action' : 'getblocknobytime',
            'timestamp' : int(time.time()),
            'closest' : 'before',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure'}
        
        return result
    except Exception as e:
        return {'result': None, 'log': e} 
    
def GetBlockBeforeTime(timestamp, url, api):
    try:
        payload = {
            'module' : 'block',
            'action' : 'getblocknobytime',
            'timestamp' : int(timestamp),
            'closest' : 'before',
            'apikey' : api
        }
        r = requests.get(url=url, params=payload)
        response = r.content
        result = json.loads(response)
        time.sleep(0.1)
        
        if result['result'] is None:
            return {'result': None, 'log': 'etherscan failure'}
        
        return result
    except Exception as e:
        return {'result': None, 'log': e}