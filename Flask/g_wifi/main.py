# Created by Bogdan Bobin
# Last Updated August 20/18 
# Version 0.7.0
################################################################
#!/usr/bin/env python3.4
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
import pandas as pd
import xlrd
#for date and time 
import datetime
import smtplib 
from email.mime.text import MIMEText 


def authorize(username, password):
  unauthorized = True
  
  while (unauthorized):

    #for authentication covering all future urllib.request uses when sending queries to ServiceNow
    url = "https://economical.service-now.com/api/now/v2/ui/table/sc_req_item" 
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
        print("Auth Error")
        sys.stdout.flush()
      
  
    unauthorized = False 
    urllib.request.install_opener(opener)
    
def record_retrieve(req_number):

    #retreive item sysid by sending a query
    idurl = "https://economical.service-now.com/sc_req_item.do?JSONv2&sysparm_action=getRecords&sysparm_query=active=true^GOTOnumberLIKE" + str(req_number) + "^ORDERBYnumber&displayvariables=true&displayvalue=true"
    req = urllib.request.Request(idurl)
    req = urllib.request.urlopen(idurl)
    data = req.read().decode()
    #print(data)
    sysrecords = json.loads(data)
    #print(sysrecords)
    sysid = sysrecords['records']
    sysid = sysid[0]
    #print(sysid)
    print("\n")
    child = sysid['variables']
    print(child)
    print("\n")
    recipient = child[0]['children'][1]['value']
    print ("On behalf of: ", recipient)
    print("\n")
    department = child[0]['children'][2]['value']
    print ("Department: ", department)
    category = child[1]
    print ("category: ",category)
    print("\n")
    child3 = child[2]
    print ("child3: ",child3)
    print("\n")
    child4 = child[3]
    print ("child4: ",child4, len(child4))
    print("\n")
    email = child[4]['children'][2]['children'][0]['value']
    print("email: " ,email)
    phone = child[4]['children'][0]['children'][0]['value']
    print ("phone: ",phone,)
    print("\n")
    child6 = child[5]
    print ("child6: ",child6, len(child6))
    print("\n")
    child7 = child[6]
    print ("child7: ", child7)
    print("\n")
    
    #getting info from database as a dictionary using sysid
    try:
      geturl = "https://economical.service-now.com/sc_req_item.do?JSONv2&sysparm_sys_id=" + str(sysid['sys_id']) +"&displayvalue=true"
    except IndexError:
      print( "REQ record: "+ str(asset_tag[i]) + " not found" )
      

    formreq = urllib.request.Request(geturl)
    formreq = urllib.request.urlopen(geturl)
    str_raw = formreq.read().decode()
    raw = json.loads(str_raw)
    values = raw['records']
    info = values[0]
  
    #for reference of response
    test = open("asset_data.txt", "w")
    test.write(str(values[0]))
    test.close()
    
    
authorize("irg", "N0vember24")
record_retrieve("RITM0072297")
    
    
    
    
    
