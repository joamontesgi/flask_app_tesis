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




app = Flask(__name__)

#Render form in HTML
@app.route('/')
def template():
    iface_names=os.listdir('/sys/class/net/')
    print(iface_names)
    return render_template('form.html', iface_names=iface_names)

@app.route('/subirPCAP')
def pcap():
    return render_template('subirPcap.html')

@app.route('/upload', methods=['POST'])
def upload():
    pcap = request.files['pcap']
    pcap_name = pcap.filename
    os.system('cicflowmeter -f ' + pcap_name + ' -c ' + pcap_name + '.csv')
    return render_template('OK.html')
    


@app.route('/algoritmo', methods=['POST'])
def algoritmo():
    algoritmo = request.form['algoritmo']
    trafico=request.form['trafico']
    interface=request.form['iface']
    tiempo=request.form['tiempoCaptura']
    if(trafico=="1"):        
        now = datetime.now()
        params = "timeout 20 tcpdump -i eth0 -w" + now.strftime("%Y%m%d-%H%M%S") + ".pcap"
        a=os.system(params)
        nombre=now.strftime("%Y%m%d-%H%M%S")
        a=os.system('sudo timeout '+tiempo+' tcpdump -i '+ interface +' -w '+nombre+'.pcap')
        os.system("sudo pkill -f getTraffic.py")
        mensaje="Trama capturada"
        return render_template('subirPcap.html', mensaje=mensaje)
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)