from datetime import datetime
import time
import os
import random

n=True
def captura(interface):
    tiempo="30"
    now = datetime.now()
    nombre=now.strftime("%Y%m%d-%H%M%S")
    a=os.system('sudo timeout '+tiempo+' tcpdump -i '+ interface +' -w '+nombre+'.pcap')
    return nombre

def conversion(name):
    os.system('cicflowmeter -f ' + name + '.pcap -c ' + name + '.csv')
    mensaje="GG"
    return mensaje


