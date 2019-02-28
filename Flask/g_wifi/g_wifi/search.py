#!/usr/bin/env python3.4
#import main
# Import modules for CGI handling 
import cgi, cgitb 
import sys , traceback

#import paramiko
#import time
#import edit
#import show
#import runcommand
#import emailout
#import checkstatus2
#import commandx
import testshow

#hours="120"
#search = sys.argv[1].lower()
#search="tho.huynh@economical.com"
#username = sys.argv[2]
#password = sys.argv[3]
#hours ="31536000"
#hours ="15552000"
#hours ="11826000"
#hours ="10368000"
#hours ="7776000"
#hours ="5184000"
#hours ="2592000"
#hours ="1209600"


def search(useremail):
    username1="thh"
    password1="Wongsun9"
    guestusername="tho.huynh@economical.com"
    guestpassword="ded3R51"
    requestnumber="test"
    host1="10.200.254.250"
    host2="10.208.254.250"
    command = "show netuser detail " + guestusername + "\n"
    commandx ='config paging disable \n'
    
    if useremail == 'empty':
        command ="show netuser summary \n"
    else :
        command = "show netuser detail " + useremail + "\n"
    prod = testshow.testeditconfig (host1,username1,password1,commandx,command,useremail)
    return prod