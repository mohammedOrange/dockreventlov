import json
#import formencode #pour convertir un multidict en json ==> git clone git://github.com/formencode/formencode.git
import time, datetime
import sqlite3
import socket
import requests
from psutil import virtual_memory


#filter : https://github.com/mitmproxy/mitmproxy/blob/master/examples/simple/filter_flows.py

data        = None
array       = []
liste       = []
url         = "https://192.168.0.2:4443/sdpweatherapi/addinstant.php"
starttime   = time.time()
hostname    = socket.gethostname()

def response(flow):
    ip = flow.server_conn.ip_address
    #local time
    #  ts = time.time()
    #  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    # print(st)
    #for key in flow.request.query:
        #ajouter un filtre pour ne récuperer que les élements souhaités
    # print(key+" = "+flow.request.query.get(key))
    if flow.request.query.get('mime') != None:
        slength = flow.response.headers.get('content-length') 	# length of package (byte)
        flength = float(slength)/1024 				# length in Kibibyte (byte/1024)
        typeObject = flow.request.query.get('mime')
        dict = {}
        dict = {
            'name':         hostname,
            'Header':       'VideoPlayBack',
            'starttime':    round(starttime),
            'timestamp':    round(time.time()),
            'url':          flow.request.headers.get('referer'),
            'ip':           str(ip),
            'player':       flow.request.query.get('itag'), 
            'type':         typeObject, 
            'numPaquet':    flow.request.query.get('rn'), 
            'bufferDispo':  flow.request.query.get('rbuf'), 
            'taillePaquet': round(flength,2)     
        } 
        print("insert mime..")
        liste.append(dict)
    elif flow.request.query.get('state') != None:
        dict ={}
        dict = {
            'name':         hostname,
            'Header':       'Stats',
            'starttime':    round(starttime),
            'timestamp':    round(time.time()),
            'url':          flow.request.headers.get('referer'),
            'ip':           str(ip),
            'player':       flow.request.query.get('cplayer'), 
            'state':        flow.request.query.get('state'), 
            'navigateur':   flow.request.query.get('cbr')        
        }
        print("insert state..")
        liste.append(dict)
    else:
        typeObject = None
        # print('array: ',array)
        mem = virtual_memory()
        memFree = mem.free/1024 #byte
        time.sleep(1)
        #	conn.commit()
        #	cursor.close()


def send_data(data):
    requests.packages.urllib3.disable_warnings()
    resp = requests.post(url, data=data, allow_redirects=True, verify=False) 
    print(resp.text)

#procédure qui s'active au démarrage programme
def start():
    print("============================ début script ============================")


#procédure qui s'active lorsque l'on met fin au programme
def done():
    print("============================ fin du script ============================")
    #print('array: ',array)
    #print(array)
    #print(json.dumps(liste))
    while True:
        input("Press Enter to continue...")
        send_data(json.dumps(liste))

