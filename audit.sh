#!/bin/bash
#Program Shell
#
cd /home/stephen
activate(){
	. /home/stephen/my_env/bin/activate
	python3 /home/stephen/eth-audit/main.py
}
activate
