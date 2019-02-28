# Created by Bogdan Bobin
# Last Updated January 22/19 
# Version 0.7.9
################################################################

#print("conntect")
import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")
#for system interaction 
import sys
#for http interaction 
import json
import urllib
#for reading excel data, pandas requires xlrd
#import pandas as pd
#import xlrd
#for date and time 
import datetime
import string
import random 
import smtplib 
from email.mime.text import MIMEText 


def authorize(username, password):
    unauthorized = True

    while (unauthorized):

    #for authentication covering all future urllib.request uses when sending queries to ServiceNow
        url="https://economical.service-now.com/api/now/v2/ui/table/sc_req_item" 
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        top_url = "https://economical.service-now.com/"
        password_mgr.add_password(None, top_url, username , password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        try:
          opener.open(url)
        except urllib.request.HTTPError as err:
          #stop code if auth fails
          if (err.code == 401):
            return -1
          

        unauthorized = False 
        urllib.request.install_opener(opener)
    return 0

def record_retrieve(req_number, duration):
    curr_date = datetime.datetime.now()                             
    info = {}
    info['ritm_not_found'] = "false"
    info['fail'] = "false"
    info['approval'] = "false"
    info['email_invalid'] = "false"
    
    #retreive item sysid by sending a query
    idurl = "https://economical.service-now.com/sc_req_item.do?JSONv2&sysparm_action=getRecords&sysparm_query=active=true^GOTOnumberLIKE" + str(req_number) + "^ORDERBYnumber&displayvariables=true&displayvalue=true"
    req = urllib.request.Request(idurl)
    req = urllib.request.urlopen(idurl)
    data = req.read().decode()
    #print(data)
    data = json.loads(data)
    data = data['records']
    try:
        data = data[0]
    except(IndexError):
        info['ritm_not_found'] = "true"
        return info
    child = data['variables']
    #print(child)
    try:                                        #try to pull all relevent data, if fails, wrong type of RITM or ServiceNow layout changed
        sponsor_name = child[0]['children'][0]['value']
        recipient = child[0]['children'][1]['value']
        department = child[0]['children'][2]['value']
        email = child[4]['children'][2]['children'][0]['value']  
        phone = child[4]['children'][0]['children'][0]['value']
        details = child[6]['children'][0]['value']
    except(KeyError, IndexError):
        info['fail'] = "true"
        return info
    try:
        company = email.rsplit('@', 1)[1]
        company = company.rsplit('.', 1)[0]
    except(IndexError):
        info['email_invalid'] = "true"
        return info
        
    if(int(duration) > 604800):
        info['approval'] = "needed"
    today = datetime.datetime.today().weekday()
    if(duration == 604800 and (today == 2 or today == 3 or today == 4)):  # 0=Monday 7=Sunday
        duration = duration + ((7-today)*86400)  #give time until next friday when run midweek or later 
    
    #print all pulled info
    print ("Opened by : ", sponsor_name)    
    print ("On behalf of: ", recipient) 
    print ("Department: ", department)  
    print("email: " ,email)
    print ("phone: ",phone)
    print ("company: ", company)
    print("Details: ", details)
    
    #set all info to dict for transfering data
    info['guest_email'] = email.lower() 
    info['s_dept'] = department 
    info['sponser_name'] = sponsor_name 
    info['guest_name'] = recipient  
    info['guest_phone'] = phone
    info['company'] = company 
    info['details'] = details 
    info['duration_seconds'] = duration
    info['time_active'] = datetime.timedelta(seconds=duration)
    info['end_date'] = curr_date + info['time_active']
   
    return info

    
def pass_gen(size = 8, chars='abcdefghjkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ' + string.digits + '!@#$%^&*()'):
    return ''.join(random.choice(chars) for _ in range(size))


def update_records(ritm):
	#will only find active RITMs, if it is closed it will not find anything
    idurl = "https://economical.service-now.com/sc_req_item.do?JSONv2&sysparm_action=getKeys&sysparm_query=active=true^GOTOnumberLIKE"+ str(ritm) +"^ORDERBYnumber&displayvariables=true&displayvalue=true"
    req = urllib.request.Request(idurl)
    req = urllib.request.urlopen(idurl)
    data = req.read().decode()
    sysrecords = json.loads(data)
    #print(sysrecords)
    sysid = sysrecords.get("records")
    sysid = sysid[0]
    print(sysid)
    new = {"state" : "1"}                               #4=Closed Incomplete, 3= Closed, 2= Work in Progress, 1= Open, -5=Pending
    #updating records with html PUT request
    updateurl = 'https://economical.service-now.com/api/now/v1/table/sc_req_item/' + str(sysid)
    update = urllib.request.Request(updateurl, data=bytes(str(new), 'utf-8'), method='PUT')
    update.add_header('Content-Type', 'application/json;charset=utf-8')
    update.add_header('Accept', 'application/json')
    urllib.request.urlopen(update)








