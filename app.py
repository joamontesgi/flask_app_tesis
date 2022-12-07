from flask import Flask, jsonify, request, render_template, make_response
import netifaces as ni
from pprint import pprint
from datetime import datetime
import time
import os
import netifaces as ni
from pprint import pprint
import netifaces as ni
import time
import datetime
from datetime import datetime
import time
import pdfkit

app = Flask(__name__)

@app.route("/pdf",methods=['POST'])
def index():
    benigno=request.form['benigno']
    DDoS=request.form['DDoS']
    DoSGoldenEye=request.form['DoSGoldenEye']
    DoSHulk=request.form['DoSHulk']
    DoSSlowhttptest=request.form['DoSSlowhttptest']
    DoSSslowloris=request.form['DoSSslowloris']
    now = datetime.now()
    nombre=now
    html = render_template(
        "certificate.html",
        benigno=benigno, nombre=nombre,DDoS=DDoS, DoSGoldenEye=DoSGoldenEye,  DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response
 


@app.route('/modelo', methods=['POST'])
def modelos():
    csv = request.files['csv']
    model = request.form['model']
    if (model=="nn"):
        from models.red_neuronal import redNeuronal
        benigno, DDoS,  DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris=redNeuronal(csv)
        return render_template('graficas.html', benigno=benigno, DDoS=DDoS,  DoSGoldenEye=DoSGoldenEye, DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris)
    elif (model=="cnn"):
        from models.red_neuronal_conv import redNeuronalconvolucional
        benigno, DDoS,  DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris=redNeuronalconvolucional(csv)
        return render_template('graficas.html', benigno=benigno, DDoS=DDoS,  DoSGoldenEye=DoSGoldenEye, DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris)
    elif (model=="svm"):
        from models.SVM import SVM
        benigno, DDoS,  DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris=SVM(csv)
        return render_template('graficas.html', benigno=benigno, DDoS=DDoS,  DoSGoldenEye=DoSGoldenEye, DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris)
    else: 
        import sys
        import importlib
        import os
        import dill
        os.system('pyenv local 3.7.13')
        os.system('python knn.py')
        from knn import KNN
        benigno, DDoS,  DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris=KNN(csv)
        return render_template('graficas.html', benigno=benigno, DDoS=DDoS,  DoSGoldenEye=DoSGoldenEye, DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris),os.system('pyenv local 3.8.5')
  


@app.route('/')
def template():
    iface_names=os.listdir('/sys/class/net/')
    print(iface_names)
    return render_template('home.html', iface_names=iface_names)

@app.route('/form')
def form():
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
        import os
        tiempo=request.form['tiempoCaptura']
        now = datetime.now()
        nombre=now.strftime("%Y%m%d-%H%M%S")
        os.system('sudo timeout '+tiempo+' tcpdump -i '+ interface +' -w '+nombre+'.pcap')
        mensaje="Trama capturada"
        return render_template('subirPcap.html', mensaje=mensaje)
    else:
        from automatico import captura, conversion
        n=True
        while(n):
            pcap_name=captura(interface)
            conversion(pcap_name)
            from files import find_csv, find_pcap
            import os
            csv=find_csv()
            pcap_name=find_pcap()
            from models.red_neuronal import redNeuronal
            benigno, DDoS,  DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris=redNeuronal(csv)
            if(benigno<DDoS or benigno<DoSGoldenEye or benigno<DoSHulk or benigno<DoSSlowhttptest or benigno<DoSSslowloris):
                from alerta import enviarMensaje
                enviarMensaje()
                os.system(' mv '+pcap_name+' '+'captures')
                os.system(' mv '+csv+' '+'captures')
                return render_template('graficas.html', benigno=benigno, DDoS=DDoS,  DoSGoldenEye=DoSGoldenEye, DoSHulk=DoSHulk, DoSSlowhttptest=DoSSlowhttptest, DoSSslowloris=DoSSslowloris)
                break
            else:
                os.system(' mv '+pcap_name+' '+'captures')
                os.system(' mv '+csv+' '+'captures')




if __name__ == '__main__':
    app.run(debug=True, port=5000)
