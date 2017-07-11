#!/usr/bin/python3

import requests
import json

url = "https://192.168.0.2:4443/sdpweatherapi/addinstant.php"

liste = []
dataA = {"name": "Olivier", "age": 30}
liste.append(dataA)
dataB = {"name": "Oli", "age": 40}
liste.append(dataB)

data = json.dumps(liste, ensure_ascii = 'False')
#print(liste)
#print(data)

requests.packages.urllib3.disable_warnings()
req = requests.post(url, data=data, allow_redirects=True, verify=False)

print(req.text)
