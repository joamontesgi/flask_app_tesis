from flask import Flask, jsonify, request, render_template
import netifaces as ni
from pprint import pprint
from datetime import datetime
import time
import os
import netifaces as ni
from pprint import pprint
import netifaces as ni
import time
import random
import datetime
from datetime import datetime
import time




app = Flask(__name__)

#@app.route('/demon', methods=['GET'])
#def demonio():
    #import demonio
    # call to real.py
    #pcap_name=real.captura()
    #real.conversion(pcap_name)
    #return jsonify({'message': 'ok'})



#Render form in HTML
@app.route('/')
def template():
    iface_names=os.listdir('/sys/class/net/')
    print(iface_names)
    return render_template('form.html', iface_names=iface_names)

@app.route('/subirPCAP')
def pcap():
    return render_template('subirPcap.html')
    
@app.route('/convertir')
def mostrar():
    return render_template('convertidoToCSV.html')

@app.route('/convertToCSV', methods=['POST'])
def upload():
    pcap = request.files['pcap']
    pcap_name = pcap.filename
    os.system('cicflowmeter -f ' + pcap_name + ' -c ' + pcap_name + '.csv')
    mensaje="Se ha convertido correctamente a CSV"
    return render_template('convertidoToCSV.html' ,mensaje=mensaje)

@app.route('/algoritmo', methods=['POST'])
def algoritmo():
    demon=request.form['demon']
    interface=request.form['iface']
    if(demon=="0"):     
        tiempo=request.form['tiempoCaptura']
        now = datetime.now()
        nombre=now.strftime("%Y%m%d-%H%M%S")
        a=os.system('sudo timeout '+tiempo+' tcpdump -i '+ interface +' -w '+nombre+'.pcap')
        mensaje="Trama capturada"
        return render_template('subirPcap.html', mensaje=mensaje)
    else:
        from demonio import captura, conversion
        n=True
        while(n):
            pcap_name=captura(interface)
            conversion(pcap_name)   
            a=(random.randint(1,2))
            if(a==1):
                print("Hay un ataque")
                #from os import remove
                #remove(pcap_name + '.pcap')
            break
        from twilio.rest import Client
        sid = 'ACc9bb3ffdd2ba8d6d57e249462c42bc25'
        auth_token='06c42c023d8699a7f93fa30d79d6832b'
        client = Client(sid, auth_token)

        client.messages.create(body='En este momento se presenta una sospecha de ataque',from_='+13466447534',to='+573042378114')


        mensaje="F"
        return render_template('ataque.html', mensaje=mensaje)


if __name__ == '__main__':
    app.run(debug=True, port=5000)