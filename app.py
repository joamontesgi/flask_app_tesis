from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from flask import Flask, jsonify, request, render_template, make_response
from datetime import datetime
import os
import time
import netifaces as ni
from pprint import pprint
from models.dnn import dnn
from alerta import enviarMensaje
from models.cnn import cnn
from automatico import captura, conversion
from files import find_csv, find_pcap
from langchain_block import run_langchain_blocking

app = Flask(__name__)


def _prediction_summary_cnn_dnn(
    *,
    benigno_cnn,
    DDoS_cnn,
    DoSGoldenEye_cnn,
    DoSHulk_cnn,
    DoSSlowhttptest_cnn,
    DoSSslowloris_cnn,
    benigno_dnn,
    DDoS_dnn,
    DoSGoldenEye_dnn,
    DoSHulk_dnn,
    DoSSlowhttptest_dnn,
    DoSSslowloris_dnn,
):
    cnn = (
        f"CNN — benignos={benigno_cnn}, DDoS={DDoS_cnn}, GoldenEye={DoSGoldenEye_cnn}, "
        f"Hulk={DoSHulk_cnn}, Slowhttptest={DoSSlowhttptest_cnn}, slowloris={DoSSslowloris_cnn}"
    )
    dnn = (
        f"DNN — benignos={benigno_dnn}, DDoS={DDoS_dnn}, GoldenEye={DoSGoldenEye_dnn}, "
        f"Hulk={DoSHulk_dnn}, Slowhttptest={DoSSlowhttptest_dnn}, slowloris={DoSSslowloris_dnn}"
    )
    return f"{cnn}. {dnn}."


@app.route('/models', methods=['POST'])
def models():
    csv = request.files['csv']
    benigno_cnn, DDoS_cnn, DoSGoldenEye_cnn, DoSHulk_cnn, DoSSlowhttptest_cnn, DoSSslowloris_cnn, malicious_ips = cnn(csv)
    csv.seek(0)
    benigno_dnn, DDoS_dnn, DoSGoldenEye_dnn, DoSHulk_dnn, DoSSlowhttptest_dnn, DoSSslowloris_dnn, malicious_ips_dnn = dnn(csv)
    malicious_ips = sorted(set(malicious_ips) | set(malicious_ips_dnn))
    block_report = None
    if malicious_ips:
        try:
            block_report = run_langchain_blocking(
                malicious_ips,
                _prediction_summary_cnn_dnn(
                    benigno_cnn=benigno_cnn,
                    DDoS_cnn=DDoS_cnn,
                    DoSGoldenEye_cnn=DoSGoldenEye_cnn,
                    DoSHulk_cnn=DoSHulk_cnn,
                    DoSSlowhttptest_cnn=DoSSlowhttptest_cnn,
                    DoSSslowloris_cnn=DoSSslowloris_cnn,
                    benigno_dnn=benigno_dnn,
                    DDoS_dnn=DDoS_dnn,
                    DoSGoldenEye_dnn=DoSGoldenEye_dnn,
                    DoSHulk_dnn=DoSHulk_dnn,
                    DoSSlowhttptest_dnn=DoSSlowhttptest_dnn,
                    DoSSslowloris_dnn=DoSSslowloris_dnn,
                ),
            )
        except Exception as exc:
            block_report = {
                "mode": "error",
                "actions": [],
                "message": f"LangChain/bloqueo: {exc!s}",
            }
    return render_template(
        'charts.html',
        benigno_cnn=benigno_cnn,
        DDoS_cnn=DDoS_cnn,
        DoSGoldenEye_cnn=DoSGoldenEye_cnn,
        DoSHulk_cnn=DoSHulk_cnn,
        DoSSlowhttptest_cnn=DoSSlowhttptest_cnn,
        DoSSslowloris_cnn=DoSSslowloris_cnn,
        benigno_dnn=benigno_dnn,
        DDoS_dnn=DDoS_dnn,
        DoSGoldenEye_dnn=DoSGoldenEye_dnn,
        DoSHulk_dnn=DoSHulk_dnn,
        DoSSlowhttptest_dnn=DoSSlowhttptest_dnn,
        DoSSslowloris_dnn=DoSSslowloris_dnn,
        malicious_ips=malicious_ips,
        block_report=block_report,
    )

@app.route('/')
def template():
    iface_names = os.listdir('/sys/class/net/')
    print(iface_names)
    return render_template('home.html', iface_names=iface_names)

@app.route('/form')
def form():
    iface_names = os.listdir('/sys/class/net/')
    print(iface_names)
    return render_template('form.html', iface_names=iface_names)

@app.route('/load_pcap')
def pcap():
    return render_template('load_pcap.html')

@app.route('/convert')
def mostrar():
    return render_template('convert_to_csv.html')

@app.route('/convert_to_csv', methods=['POST'])
def upload():
    pcap = request.files['pcap']
    pcap_name = pcap.filename
    os.system('cicflowmeter -f ' + pcap_name + ' -c ' + pcap_name + '.csv')
    mensaje = "Se ha convertido correctamente a CSV"
    return render_template('convert_to_csv.html', mensaje=mensaje)


@app.route('/real_time', methods=['POST'])
def algoritmo():
    demon = request.form['demon']
    interface = request.form['iface']
    if demon == "0":
        tiempo = int(request.form['capture_time'])
        tiempo = tiempo * 60  # en segundos
        nombre = datetime.now().strftime("%Y%m%d-%H%M%S")
        os.system('sudo timeout ' + str(tiempo) + ' tcpdump -i ' + interface + ' -w ' + nombre + '.pcap')
        mensaje = "Trama capturada"
        return render_template('load_pcap.html', mensaje=mensaje)
    else:
        sid = request.form['sid']
        token = request.form['token']
        numero_cel = request.form['numero_cel']
        twi = request.form['twi']
        mensaje = request.form['mensaje']
        hora_inicio = datetime.now()
        fecha = hora_inicio.strftime("%Y-%m-%d")
        while True:
            pcap_name = captura(interface)
            conversion(pcap_name)
            csv = find_csv()
            pcap_name = find_pcap()
            benigno, DDoS, DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris, malicious_ips_cnn = cnn(csv)
            benigno_dn, DDoS_dn, DoSGoldenEye_dn, DoSHulk_dn, DoSSlowhttptest_dn, DoSSslowloris_dn, malicious_ips_dnn = dnn(csv)
            malicious_ips = sorted(set(malicious_ips_cnn) | set(malicious_ips_dnn))
            cnn_attack = DDoS > 0 or DoSGoldenEye > 0 or DoSHulk > 0 or DoSSlowhttptest > 0 or DoSSslowloris > 0
            dnn_attack = (
                DDoS_dn > 0
                or DoSGoldenEye_dn > 0
                or DoSHulk_dn > 0
                or DoSSlowhttptest_dn > 0
                or DoSSslowloris_dn > 0
            )
            if cnn_attack or dnn_attack:
                enviarMensaje(sid, token, mensaje, numero_cel, twi)
                block_report = None
                if malicious_ips:
                    try:
                        block_report = run_langchain_blocking(
                            malicious_ips,
                            _prediction_summary_cnn_dnn(
                                benigno_cnn=benigno,
                                DDoS_cnn=DDoS,
                                DoSGoldenEye_cnn=DoSGoldenEye,
                                DoSHulk_cnn=DoSHulk,
                                DoSSlowhttptest_cnn=DoSSlowhttptest,
                                DoSSslowloris_cnn=DoSSslowloris,
                                benigno_dnn=benigno_dn,
                                DDoS_dnn=DDoS_dn,
                                DoSGoldenEye_dnn=DoSGoldenEye_dn,
                                DoSHulk_dnn=DoSHulk_dn,
                                DoSSlowhttptest_dnn=DoSSlowhttptest_dn,
                                DoSSslowloris_dnn=DoSSslowloris_dn,
                            )
                            + " (captura en tiempo real).",
                        )
                    except Exception as exc:
                        block_report = {
                            "mode": "error",
                            "actions": [],
                            "message": f"LangChain/bloqueo: {exc!s}",
                        }
                os.system('mv ' + pcap_name + ' captures')
                os.system('mv ' + csv + ' captures')
                hora_fin = datetime.now()
                tiempo = hora_fin - hora_inicio
                return render_template(
                    'charts.html',
                    fecha=fecha,
                    benigno=benigno,
                    DDoS=DDoS,
                    DoSGoldenEye=DoSGoldenEye,
                    DoSHulk=DoSHulk,
                    DoSSlowhttptest=DoSSlowhttptest,
                    DoSSslowloris=DoSSslowloris,
                    tiempo=tiempo,
                    malicious_ips=malicious_ips,
                    block_report=block_report,
                )
            else:
                os.system('mv ' + pcap_name + ' captures')
                os.system('mv ' + csv + ' captures')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
