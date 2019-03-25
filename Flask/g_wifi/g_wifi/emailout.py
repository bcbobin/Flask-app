#!/usr/bin/env python3.4
import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")
import smtplib 
from email.mime.text import MIMEText 

def emailsponsor (subjectx,messagex,sponsoremail):
    sponsoremail1=sponsoremail
    destination = sponsoremail1
    
    whofrom = 'networkgroup@economical.com'
    msg = MIMEText(messagex)

    msg['Subject'] = subjectx
    msg['To'] = destination
    msg['From'] = whofrom
    s = smtplib.SMTP('mail01.economicalinsurance.com')
    s.send_message(msg)
    s.quit()

    
#testing = emailsponsor ('testing sub','messages' ,'tho.huynh@economical.com')  
