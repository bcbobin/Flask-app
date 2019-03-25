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
import auth
import read_update
import email

def run_update(username, password, filename, userEmail): 
  now = datetime.datetime.now()
#declare some variables for dataToSendBack so they can be set to (+=) and added to (++)
  dataToSendBack = {}
  dataToSendBack["assetsFailed"] = 0							#acts as "pass-by-reference"
  dataToSendBack["DNE"] = ""
  dataToSendBack["duplicate"] = ""
  dataToSendBack["multiple_records"] = "False"
  dataToSendBack["notFound"] = "False"
  dataToSendBack["finished"] = "False"
  dataToSendBack["excel"] = ""
  auth_value = auth.authorize(username, password, dataToSendBack, userEmail, now)
  if(auth_value == -1):
    return dataToSendBack
  print("auth")
  read_update.read_excel(filename, username, dataToSendBack, userEmail, now)
  if(auth_value == -1):
    return dataToSendBack
  print("excel")
  
  #to end the script, send the user an email and print info if needed by using echo in php
  dataToSendBack["finished"] = "True"
  print(dataToSendBack)
  sys.stdout.flush()
  #message = email_user.email_message(dataToSendBack)
  #email_user.emailsponsor(message, userEmail, now)
  return dataToSendBack