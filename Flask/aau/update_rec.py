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

def update_records(new, sysid, dataToSendBack):
    #updating records with html PUT request
    #also change if tested outside of production 
    updateurl = 'https://economical.service-now.com/api/now/v1/table/alm_hardware/' + str(sysid[0])
    update = urllib.request.Request(updateurl, data=bytes(str(new), 'utf-8'), method='PUT')
    update.add_header('Content-Type', 'application/json;charset=utf-8')
    update.add_header('Accept', 'application/json')
    urllib.request.urlopen(update)
    dataToSendBack["updated"] = "True"