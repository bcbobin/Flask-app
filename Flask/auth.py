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
#file imports for functions


def authorize(username, password, dataToSendBack, userEmail, now):
  unauthorized = True
  
  while (unauthorized):

    #for authentication covering all future urllib.request uses when sending queries to ServiceNow
    #this is the link for the prod ServiceNow site, change if tested outside of production 
    url = "https://economical.service-now.com/api/now/v2/ui/table/alm_hardware" 
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    #also change if tested in production 
    top_url = "https://economical.service-now.com/"
    password_mgr.add_password(None, top_url, username , password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    try:
      opener.open(url)
    except urllib.request.HTTPError as err:
      #stop code if auth fails
      if (err.code == 401):
        dataToSendBack['authorization'] = "Failed"
        dataToSendBack['finished'] = "True"
        print(dataToSendBack)
        sys.stdout.flush()
        #message = email_user.email_message(dataToSendBack)
        #email_user.emailsponsor(message, userEmail, now)
        #sys.exit()
        return -1
  
    unauthorized = False 
    urllib.request.install_opener(opener)
    dataToSendBack["authorization"] = "Passed"