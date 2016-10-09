# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json, csv 

user = 'cloudadmin@corp.local'
password = 'VMware1!'
tenant = 'vsphere.local'
vraHostname = 'vra-01a.corp.local'
headers = {'Content-Type' : 'application/json; charset=utf-8', 'Accept' : 'application/json'}

def doEntireThing():
    #global auth_headers
    #auth_headers = tokenForUsername(user)
    newBgsfromCsv = newBgsFromCsv()

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

def newBgsFromCsv():
    url = 'https://'+vraHostname+'tenants/'+tenant+'/subtenants/'
    body = {"name":"Business Group 002", "description":"", "subtenantRoles":[{"scopeRoleRef":"CSP_SUBTENANT_MANAGER", "principalId":[{"domain":"lab.local", "name":"User002000"}]},{"scopeRoleRef":"CSP_CONSUMER", "principalId":[{"domain":"lab.local", "name":"Group002"}]},{"scopeRoleRef":"CSP_SUPPORT", "principalId":[]}], "extensionData":{"entries":[{"key":"iaas-manager-emails", "value":{"type":"string", "value":"User002000@lab.local"}}, {"key":"iaas-ad-container", "value":{"type":"string", "value":""}}]}}
    with open('bgs.csv') as sfile:
        new = csv.DictReader(sfile)
        for row in new:
            body['name']=row['name']
            body['description']=row['description']
            body['subtenantRoles'][0]['principalId'][0]['domain']=row['managerDomain']
            body['subtenantRoles'][0]['principalId'][0]['name']=row['managerName']
            body['subtenantRoles'][1]['principalId'][0]['domain']=row['consumerDomain']
            body['subtenantRoles'][1]['principalId'][0]['name']=row['consumerName']
            body['extensionData']['entries'][0]['value']=row['emailTo']
            #body['primaryWinsAddress']=row['adContainer']
            req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
            print req.status_code
#	print body

if __name__ == '__main__': # Do this if the script is run standalone
    doEntireThing()


