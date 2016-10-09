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
    global getNetworkCsv
    newNetworksfromCsv = newNetworksFromCsv()

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

def newNetworksFromCsv():
    url = 'https://' + vraHostname + '/iaas-proxy-provider/api/network/profiles'
    with open('profile.json', 'r+') as pfile:
        body = json.load(pfile)
    with open('newProfiles.csv') as sfile:
        new = csv.DictReader(sfile)
        for row in new:
            body['name']=row['profileName']
            body['description']=row['profileDesc']
            body['profileType']=row['profileType']
            body['subnetMask']=row['subnetMask']
            body['gatewayAddress']=row['gatewayAddress']
            body['primaryDnsAddress']=row['primaryDns']
            body['secondaryDnsAddress']=row['secondaryDns']
            body['dnsSuffix']=row['dnsSuffix']
            body['dnsSearchSuffix']=row['dnsSearchSuffix']
            body['primaryWinsAddress']=row['primaryWins']
            body['secondaryWinsAddress']=row['secondaryWins']
            body['definedRanges'][0]['name']=row['rangeName']
            body['definedRanges'][0]['description']=row['rangeDesc']
            body['definedRanges'][0]['beginIPv4Address']=row['startIP']
            body['definedRanges'][0]['endIPv4Address']=row['endIP']
            req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
            print req.status_code

if __name__ == '__main__': # Do this if the script is run standalone
    doEntireThing()
