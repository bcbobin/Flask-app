# Created by Bogdan Bobin
# Last Updated March 8/19
# Version 0.9.1
################################################################

import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")
#for system interaction 
import sys
#for http interaction 
import json
import urllib 
from datetime import datetime
from datetime import timedelta
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
    curr_date = datetime.now()                             
    info = {}
    info['ritm_not_found'] = "false"
    info['fail'] = "false"
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
    except(KeyError, IndexError):                       #error when attempting to retrieve information
        info['fail'] = "true"
        return info
    try:
        company = email.rsplit('@', 1)[1]
        company = company.rsplit('.', 1)[0]
    except(IndexError):                                 #if guest email is not there, assumed format is blahblah@company.blah
        info['email_invalid'] = "true"
        return info
    
    #print all pulled info
    # print ("Opened by : ", sponsor_name)    
    # print ("On behalf of: ", recipient) 
    # print ("Department: ", department)  
    # print("email: " ,email)
    # print ("phone: ",phone)
    # print ("company: ", company)
    # print("Details: ", details)
    
    #set all info to dict for transfering data
    info['guest_email'] = email.lower() 
    info['s_dept'] = department 
    info['sponser_name'] = sponsor_name 
    info['guest_name'] = recipient  
    info['guest_phone'] = phone
    info['company'] = company 
    info['details'] = details 
    info['duration_seconds'] = duration
    info['time_active'] = timedelta(seconds=int(duration))              #to show time given in the email
    info['end_date'] = curr_date + info['time_active']                      # to show end date in the email     
   
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
    #print(sysid)
    new = {"state" : "1"}                               #4=Closed Incomplete, 3= Closed, 2= Work in Progress, 1= Open, -5=Pending
    #updating records with html PUT request
    updateurl = 'https://economical.service-now.com/api/now/v1/table/sc_req_item/' + str(sysid)
    update = urllib.request.Request(updateurl, data=bytes(str(new), 'utf-8'), method='PUT')
    update.add_header('Content-Type', 'application/json;charset=utf-8')
    update.add_header('Accept', 'application/json')
    urllib.request.urlopen(update)

def timeset(duration):
    curr_date = datetime.today()           #full date of today
    today = datetime.today().weekday()         #weekday 0=Monday 7=Sunday
    if(duration == "4hours"):
        duration = 14400                                #4 hours in seconds
        return duration
    if(duration == "today"):
        duration = 19 - curr_date.hour                 #19 hours minus current hour then convert hours to seconds 
        duration = duration *60*60
        return duration
    if(duration == "tomorrow"):
        duration = 19 - curr_date.hour                  #hours left until 7 pm
        duration = duration + 24                        #add 24 hours
        duration = duration*60*60                       #convert to seconds
        return duration
    if(duration == "3days"):
        duration = 259200
        return duration
    if(duration == "endofweek"):
        duration = 19 - curr_date.hour                 #hours till 7pm
        days = 5 - today                                #days till Friday
        duration = ((days*24) + duration)*60*60         # conver to seconds 
        return duration
    if(duration == "nextweek"):
        duration = 19 - curr_date.hour                 #hours till 7pm
        days = 7 - today + 5                            #place in the curent week plus 5 days to get to next friday
        duration = ((days*24) + duration)*60*60         # conver to seconds 
        return duration
    if(duration == "1year"):
        duration = 31536000         #1 year in seconds
        return duration
    else:               #custom input- date format "2019-03-35" - "yyyy-mm-dd"
        custom = datetime.strptime(duration, "%Y-%m-%d")
        diff = (custom - curr_date).seconds
        duration = int(diff) + (19*60*60)              #convert days into seconds + 19 hours to make sure it ends at 7pm on the day
        return duration

def delex_mail(sponsor, user, edit, exflag):
    recipients= []
    if exflag == "true":
        subject = "Guest wifi, user extension for "+ user
        message = "User " + sponser + "has extended " + user + "for an additional: "+ edit
        error= "If this change was a mistake, please contant the network team at networkgroup@economical.com and explain the error to be rectified"
    else:
        subject=  "Guest wifi, user: " + user + "has been deleted by: " + sponsor
        message= "A deletion was made to the guest wifi list. User " + sponsor + "has deleted: " + user
        error= "If this change was a mistake, please contant the network team at networkgroup@economical.com and explain the error to be rectified"
        
    
    



