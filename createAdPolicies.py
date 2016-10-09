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
    #global newUsersfromCsv
    #newUsersfromCsv = newUsersFromCsv()
    #global addUsersToBg
    #addUsersToBg = addUsersToBg()
    createAdPolicy()

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


def createAdPolicy():
    #url = 'https://' + vraHostname + '/advanced-designer-service/api/policies/'
    #body = {"hrid":"bu001", "description":"", "properties":{"entries":[{"key":"ext.policy.activedirectory.endpoint .id", "value":{"type":"string", "value":"#_v2_#,#RootItem#,#4e24b69c-d1e9-40ca-b9e8-0d96b92afe6f#"}} ,{"key":"ext.policy.activedirectory.domain", "value":{"type":"string", "value":"lab.local"}},{"key":"ext .policy.activedirectory.orgunit", "value":{"type":"string", "value":"ou=bu001,ou=servers,dc=lab,dc=local"}}]}}
    for i in xrange(001,101) :
    	print(i)
    	i=["{:0>3}".format(i)]
    	print(i)
    

    #req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
    #req = requests.get(url = url, headers = headers, verify = False)
    #print req.json()
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


