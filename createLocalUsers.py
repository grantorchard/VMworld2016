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
    #global newUsersfromCsv
    #newUsersfromCsv = newUsersFromCsv()
    global addUsersToBg
    addUsersToBg = addUsersToBg()

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

def newUsersFromCsv():
    url = 'https://' + vraHostname + '/identity/api/tenants/vsphere.local/principals'
    body = {'firstName': 'Please', 'lastName': 'Work', 'emailAddress': 'pleasework@corp.local', 'locked': 'false', 'disabled': 'false', 'password': 'VMware1!', 'principalId': {'domain': 'vsphere.local', 'name': 'pleasework'}, 'tenantName': 'vsphere.local', 'name': ''}
    with open('userList.csv') as sfile:
        users = csv.DictReader(sfile)
        for row in users:
            body['firstName']=row['firstName']
            body['lastName']=row['lastName']
            body['emailAddress']=row['emailAddress']
            body['password']=row['password']
            body['principalId']['domain']='vsphere.local'
            body['principalId']['name']=row['username']
            body['name']=row['firstName']+" "+row['lastName']
            req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
            print req.status_code

def addUsersToBg():
    url = 'https://' + vraHostname + '/identity/api/tenants/vsphere.local/subtenants/'
    req = requests.get(url = url, headers = headers, verify = False)
    print req.json()
    #bgId = req.id
    #url = 'https://' + vraHostname + '/identity/api/tenants/vsphere.local/subtenants/' + bgId + '/principals'
    #body = req.json()
    #userData = {"@type": "PrincipalData", "name": "Development User", "principalId": {"domain": "vsphere.local", "name": ""}, "principalType": "USER"},
    #with open('userList.csv') as sfile:
    #    users = csv.DictReader(sfile)
    #    for row in users:
    #        userData['name']=row['firstName']+" "+row['lastName']
    #        userData['principalId']['name']=row['username']
    #        body.append(userData)
    #req = requests.put(url, headers = auth_headers, verify = False, data=json.dumps(body))


if __name__ == '__main__': # Do this if the script is run standalone
    doEntireThing()
