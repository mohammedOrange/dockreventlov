import json
#import formencode #pour convertir un multidict en json ==> git clone git://github.com/formencode/formencode.git
import time, datetime
import sqlite3
import socket
# from psutil import virtual_memory
import psutil


#filter : https://github.com/mitmproxy/mitmproxy/blob/master/examples/simple/filter_flows.py

data = None
array = []

def response(flow):
	ip = flow.server_conn.ip_address
	#local time
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
	print(st)
	for key in flow.request.query:
		#ajouter un filtre pour ne récuperer que les élements souhaités
		print(key+" = "+flow.request.query.get(key))
	if flow.request.query.get('mime') != None:
		slength = flow.response.headers.get('content-length') 	# length of package (byte)
		flength = float(slength)/1024 				# length in Kibibyte (byte/1024)
		typeObject = flow.request.query.get('mime')
		data = json.dumps({
                    'Header':'VideoPlayBack',
                    'timestamp':round(ts),
                    'url':flow.request.headers.get('referer'),
                    'ip':str(ip),
                    'player':flow.request.query.get('itag'), 
                    'type':typeObject, 
                    'numPaquet':flow.request.query.get('rn'), 
                    'bufferDispo':flow.request.query.get('rbuf'), 
                    'taillePaquet':round(flength,2)})
		array.append(data)
	elif flow.request.query.get('state') != None:
		data = json.dumps({
                    'Header':'Stats',
                    'timestamp':round(ts),
                    'url':flow.request.headers.get('referer'),
                    'ip':str(ip),
                    'player':flow.request.query.get('cplayer'), 
                    'state':flow.request.query.get('state'), 
                    'navigateur':flow.request.query.get('cbr')})
		array.append(data)
	else:
		typeObject = None
	print('array: ',array)
	mem = psutil.virtual_memory()
	memFree = mem.free/1024 #byte
	time.sleep(1)
#	conn.commit()
#	cursor.close()


#procédure qui s'active au démarrage programme
def start():
	print("============================ début script ============================")



#procédure qui s'active lorsque l'on met fin au programme
def done():
	print("============================ fin du script ============================")
	print('array: ',array)
	PROCNAME = "mitmdump"
	for proc in psutil.process_iter():
		if proc.name() == PROCNAME:
			proc.kill()
	#send data