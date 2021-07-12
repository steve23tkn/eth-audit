infura_api = 'https://mainnet.infura.io/v3/b000000000000000000000000000' # INFURA API
apix = '' # INFURA SECRET KEY
urlx = 'https://api.etherscan.io/api'

pool_addr = '0x50fdf2380a356d76f949c45efc2d26e005f48936' # TARGET ADDRESS

HOST = 'localhost'
USER = 'root'
PASS = ''
db_name = 'audit'

block_one = 12177896 # FIRST BLOCK OF THIS ACCOUNT - CAN BE CHECKED USING using: etherscan/GetFirstTx

step = 100_000 # TO PARTITION RETURNED JSON UNDER < 10K LIST
delay = 3600 # RUN WORKER EVERY 3600SEC = 1HR