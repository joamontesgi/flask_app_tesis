import os
import glob
def find_csv():
    path = os.getcwd()
    csv = glob.glob(path + "/*.csv")
    for name in csv:
        return name

def find_pcap():
    path = os.getcwd()
    pcap = glob.glob(path + "/*.pcap")
    for name in pcap:
        return name