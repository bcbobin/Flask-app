# Created by Bogdan Bobin
# Last Updated February  19/19 
# Version 0.7.0
################################################################

import cgi, cgitb 
import sys , traceback
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
import netmiko

#if connection timeout - OSError - Socket is closed - must connectHandler again to fix

def add_user(cont1, cont2, mac, start, end):
    #config macfilter add 6c:4b:90:27:4f:a2 3 cwlan-int startdate:enddate 
    #6c:4b:90:27:4f:a2
    #error - '\nIncorrect input! <IP addr> must be a valid IP Address\n'
    
    connect1 = netmiko.ConnectHandler(**cont1)
    output1 = connect1.send_command("config macfilter add "+ str(mac) +" 3 cwlan-int " + str(start) + ":" + str(end))
    connect1.disconnect()
    
    connect2 = netmiko.ConnectHandler(**cont2)
    output2 = connect2.send_command("config macfilter add "+ str(mac) +" 3 cwlan-int " + str(start) + ":" + str(end))
    connect2.disconnect()
    
    if "Incorrect input" in output1 or output2:         #mac adresss is wrong
        return -1
    elif "already exists" in output1 and output2:       #user already exists on both controllers
        return 1
    else:                                               #nothing bad happened and finished adding user on both
        return 0

def remove_user(cont1, cont2, mac):

    connect1 = netmiko.ConnectHandler(**cont1)
    connect2 = netmiko.ConnectHandler(**cont2)
    output1 = connect1.send_command("config macfilter delete "+ mac)
    output2 = connect2.send_command("config macfilter delete "+ mac)
    connect1.disconnect()
    connect2.disconnect()
    #config macfilter delete 88:b1:11:28:e1:5f 
    
    #check if user DNE on both controllers - error
    #User 88b11128e15f does not exist.
    if "does not exist" in output1 and output2:             #using and because if exists on one, it is fine to delete and proceed 
        return -1
    else:
        return 0
    

def summary(connect):
    #show macfilter summary - not enough information, will need to pull data from custom user database
    return 0
    


