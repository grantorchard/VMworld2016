 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json, csv 

user = 'cloudadmin@corp.local'
password = 'VMware1!'
tenant = 'vsphere.local'
vraHostname = 'vra-01a.corp.local'
headers = {'Content-Type' : 'application/json; charset=utf-8', 'Accept' : 'application/json'}

def doEntireThing():
    global auth_headers
    auth_headers = tokenForUsername(user)
    createReservations()

def tokenForUsername(user):
    url = 'https://' + vraHostname + '/identity/api/tokens'
    data = {'username': user,'password': password,'tenant': tenant}
    req = requests.post(url = url, data = json.dumps(data), headers = headers, verify = False)
    body = req.json()
    tokenId = 'Bearer ' + body['id']
    if req.status_code != 200:
        print 'Authentication Failed for ' + user + ' with error text ' + req.text
    else:
        print 'Authentication Suceeded for ' + user + '.'
    headers.update({'Authorization': tokenId})
    return headers

def createReservations():
    url = 'https://' + vraHostname + '/reservation-service/api/reservations'
    with open('reservationBody.json', 'r+') as pfile:
        body = json.load(pfile)
    for i in range (2,10):
    	name = "Cluster Site A-Res-"
    	#body['name'] = "Cluster Site A-Res-" + i
    	name+=str(i)
    	body['name']=name
    	print body['name']
    	req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
    	print req.text

if __name__ == '__main__': # Do this if the script is run standalone
    doEntireThing()