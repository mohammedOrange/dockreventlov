import json
#import formencode #pour convertir un multidict en json ==> git clone git://github.com/formencode/formencode.git
import time, datetime
import sqlite3
import socket
import requests
import sys
from psutil import virtual_memory


#https://github.com/mitmproxy/mitmproxy/blob/811b72cd304a8c75efaf706fd57cfbe9494cd3d9/examples/har_extractor.py

#filter : https://github.com/mitmproxy/mitmproxy/blob/master/examples/simple/filter_flows.py

data        = None
array       = []
liste       = []
url         = "https://192.168.0.2:4443/sdpweatherapi/addinstant.php"
starttime   = time.time()
hostname    = socket.gethostname()
urlYoutube  = "https://www.youtube.com/watch?v="


def response(flow):
    ip = flow.server_conn.ip_address
    isAd  = False
    #local time
    #  ts = time.time()
    #  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    # print(st)
    #for key in flow.request.query:
        #ajouter un filtre pour ne récuperer que les élements souhaités
    # print(key+" = "+flow.request.query.get(key))
    

    if flow.request.query.get('mime') != None:
        slength = flow.response.headers.get('content-length')       # length of package (byte)
        flength = float(slength)/1024                               # length in Kibibyte (byte/1024)
        typeObject = flow.request.query.get('mime')
        dict = {}
        dict = {
                'name':         hostname,                                   # name of the hostname
                'Header':       'VideoPlayBack',                            # type of flow (video play back)
                'starttime':    round(starttime),                           # time of the beginning of the test
                'timestamp':    round(time.time()),                         # time: AAAA-MM-JJ_HH:MM:SS:ss       
                'ip':           str(ip),                                    # ip server
                'player':       flow.request.query.get('itag'),             # itag contains infos player
                'type':         typeObject,                                 # type of flow (audio, video, ...)
                'numPaquet':    flow.request.query.get('rn'),               # number of the paquet
                'bufferDispo':  flow.request.query.get('rbuf'),             # buffer length 
                'taillePaquet': round(flength,2),                           # 
                'cpn':          flow.request.query.get('cpn')               # cpn -> id of the session playback
                } 
        #  print("insert mime..")
        liste.append(dict)
        print(dict)
    elif flow.request.query.get('state') != None:
            #if the docid (id of the video) is different to the url of the video requested (in parameter)
            #   it's an add
        tmp = urlYoutube + flow.request.query.get('docid')
        if urlYoutube + flow.request.query.get('docid') == sys.argv[1]:
            print(tmp)
            isAd =    False
        else:
            isAd =    True

        dict ={}
        dict = {
                'name':         hostname,                                   # name of the hostname
                'Header':       'Stats',                                    # type of flow (stats)
                'starttime':    round(starttime),                           # time of the beginning of the test
                'timestamp':    round(time.time()),                         # time: AAAA-MM-JJ_HH:MM:SS:ss
                'idVideo':      flow.request.query.get('docid'),            # video id 
                'ip':           str(ip),                                    # ip server
                'player':       flow.request.query.get('cplayer'),          # player (often UNIPLAYER)
                'state':        flow.request.query.get('state'),            # state of playback (nothing if no problem)
                'navigateur':   flow.request.query.get('cbr'),              # browser name
                'cpn':          flow.request.query.get('cpn'),              # cpn -> id of the session playback 
                'isAd':         isAd                                       # is an add or not
                }
        #  print("insert state..")
        liste.append(dict)
        print(dict)
    else:
        typeObject = None
        # print('array: ',array)
        mem = virtual_memory()
        memFree = mem.free/1024 #byte
#        time.sleep(1)


def send_data(data):
    #  print(data)
    requests.packages.urllib3.disable_warnings()
    resp = requests.post(url, data=data, allow_redirects=True, verify=False) 
    print(resp.text)

#procédure qui s'active au démarrage programme
def start():
    print("============================ début script ============================")


#procédure qui s'active lorsque l'on met fin au programme
def done():
    print("============================ fin du script ===========================")
    #print('array: ',array)
    #print(array)
    #  print(json.dumps(liste))
    while True:
        input("Press Enter to continue...")
        print(json.dumps(liste))
        send_data(json.dumps(liste))

