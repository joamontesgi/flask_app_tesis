import os
from datetime import datetime
import time
now = datetime.now()
params = "timeout 20 tcpdump -i eth0 -w" + now.strftime("%Y%m%d-%H%M%S") + ".pcap"
a=os.system(params)


