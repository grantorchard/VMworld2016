# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json

user = 'cloudadmin@corp.local'
password = 'VMware1!'
tenant = 'vsphere.local'
vraHostname = 'vra.corp.local'
headers = {'Content-Type' : 'application/json; charset=utf-8', 'Accept' : 'application/json'}

def doEntireThing():
    global auth_headers
    global networkProfileName
    global networkProfileId
    global computeResources
    global networkPathLabel
    global networkPath
    global updatedNetworkBody
    global reservationsToUpdate
    auth_headers = tokenForUsername(user)
    networkProfileName = postNetworkProfile()
    networkProfileId = getNetworkProfileId()
    networkPathLabel = 'vMotion Network'
    computeResources = getComputeResourceIds()
    networkPath = getNetworkPathId()
    updatedNetworkBody = updateNetworkBody()
    reservationsToUpdate = getReservations()
    updateReservations()

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


def postNetworkProfile():
    url = 'https://' + vraHostname + '/iaas-proxy-provider/api/network/profiles'
    with open('profile.js', 'r+') as sfile:
        body = json.load(sfile)
    req = requests.post(url, headers = auth_headers, verify = False, data=json.dumps(body))
    if req.status_code != 201:
        #for items in req.text
        print 'Network Profile creation failed with error text ' + req.text
    else:
        print 'Network Profile ' + body['name'] + ' Successfully Created.'
    return body['name']

def getNetworkProfileId():
    url = 'https://' + vraHostname + '/iaas-proxy-provider/api/network/profiles?$filter=(name eq \'' + networkProfileName + '\')'
    req = requests.get(url, headers = auth_headers, verify = False)
    body = req.json()
    for profile in body['content']:
        return profile['id']    

def getComputeResourceIds():
    url = 'https://' + vraHostname + '/reservation-service/api/data-service/schema/Infrastructure.Reservation.Virtual.vSphere/default/computeResource/values'
    req = requests.post(url, headers = auth_headers, verify = False, data='{}')
    body = req.json()
    computeResourceIds = []
    for item in body[u'values']:
        if item['label'] == 'Cluster Site A (vCenter)':
            computeResourceIds.append(item['underlyingValue']['id'])
            print 'Compute Resource with ID ' + item['underlyingValue']['id'] + ' found'
    return computeResourceIds


def getNetworkPathId():
    url = 'https://' + vraHostname + '/reservation-service/api/data-service/schema/Infrastructure.Reservation.Virtual.vSphere/default/reservationNetworks/values'
    req = requests.post(url, headers = auth_headers, verify = False, data='{"text":"Element","dependencyValues":{"entries":[{"key":"computeResource","value":{"type":"entityRef","componentId":null,"classId":"ComputeResource","id":"2183b391-b057-429b-b163-bb258a0ff868","label":"Cluster Site A (vCenter)"}}]},"associateValue":null}')
    body = req.json()
    #print body
    for item in body[u'values']:
        if item['label'] == networkPathLabel:
            for key in item['underlyingValue']['values']['entries']:
                return key['value']['id']
    print 'Network Path '  + networkPathLabel + ' found with ID ' + key['value']['id']

def updateNetworkBody():
    with open('networkBody.js', 'r+') as sfile:
        networkBody = json.load(sfile)
        print networkBody
    for item in networkBody['values']['entries']:
        if item['key'] == 'networkPath':
            item['value']['id'] = networkPath
            item['value']['label'] = networkPathLabel
        else:
            item['value']['id'] = networkProfileId 
            item['value']['label'] = networkProfileName 
    return networkBody
    print networkBody

def getReservations():   
    url = 'https://' + vraHostname + '/reservation-service/api/reservations'
    req = requests.get(url, headers = auth_headers, verify = False)
    body = req.json()
    reservations = []
    for computeResourceId in computeResources:
        for reservation in body['content']:
            for resourceType in reservation['extensionData']['entries']:
                if resourceType['key'] == 'computeResource':
                    if resourceType['value']['id'] == computeResourceId:
                        reservations.append(reservation['id'])
    return reservations

def updateReservations():   
    for reservation in reservationsToUpdate:
        print 'Updating Reservation with ID ' + reservation + ' with new network path and profile information.'
        url = 'https://' + vraHostname + '/reservation-service/api/reservations/' + reservation
        req = requests.get(url, headers = auth_headers, verify = False)
        body = req.json()
        #print body 
        #print req.encoding
        for resourceType in body['extensionData']['entries']:
            if resourceType['key'] == 'reservationNetworks':
                resourceType['value']['items'].append(updatedNetworkBody)
            #print body
        req = requests.put(url, headers = auth_headers, verify = False, data=json.dumps(body))
        print req.text

if __name__ == '__main__': # Do this if the script is run standalone
    doEntireThing()
