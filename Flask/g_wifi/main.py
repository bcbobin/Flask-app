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
from datetime import datetime
import string
import random 
import smtplib 
from email.mime.text import MIMEText 

    #TODO- Tho - web html bug, looks weird on a 17 inch monitor 
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

def record_retrieve(req_number):
    curr_date = datetime.now()                             
    info = {}
    info['ritm_not_found'] = "false"
    info['fail'] = "false"
    info['approval'] = "false"
    info['email_invalid'] = "false"
    info['invalid_date'] = "false"
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
        start_date = child[5]['children'][0]['value']
        end_date = child[5]['children'][2]['value']
        info['start_date'] = start_date                          #add the values to dict before they get changed 
        info['end_date'] = end_date
        start_date = start_date.rsplit(' ', 1)[0]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = end_date.rsplit(' ', 1)[0]
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
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
    
    print ("Opened by : ", sponsor_name)    
    print ("On behalf of: ", recipient) 
    print ("Department: ", department)  
    print("email: " ,email)
    print ("phone: ",phone)
    print ("company: ", company)
    print ("Start: ",start_date)
    print ("End: ", end_date)
    print("Details: ", details)
    print ("Curr date: ", curr_date)
    
    info['guest_email'] = email.lower() 
    info['s_dept'] = department 
    info['sponser_name'] = sponsor_name 
    info['guest_name'] = recipient  
    info['guest_phone'] = phone
    info['company'] = company 
    info['details'] = details 
    
    
    days = (end_date - start_date)
    seconds = days.total_seconds()
    if(seconds > 604800):
        info['approval'] = "needed"
    if(seconds == 0):
        seconds = 86400
    actual_seconds = end_date - curr_date
    if (actual_seconds < 0):
        info['invalid_date'] = "true"
    actual_seconds = actual_seconds.total_seconds()
    info['duration_seconds'] = int(actual_seconds)
    print("Seconds: ", actual_seconds, "\n")
    
    return info

    
def pass_gen(size = 8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def update_records(ritm):
    #possibly call auth from here with other credientials 
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





#authorize("irg", "")
#record_retrieve("RITM0072297")
#TODO- ask what credectials to use when authorizing and closing the request






