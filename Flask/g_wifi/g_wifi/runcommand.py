#!/usr/bin/env python3.4
# Import modules for CGI handling 
import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")
import os
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()
def runcommand (host1,username1,password1,command):
    host=host1
    username=username1
    password=password1
    #interface ="no value was found at central, please verify Device is connected to LAN NO WIRELESS"
    #interface = "1"
    ssh.connect(host1,username=username1,password=password1)
    stdin, stdout, stderr = ssh.exec_command (command)
    stdin.close()
    
    for line in stdout.readlines():
        #print (line)
        if "switchport access vlan" in line:
            print(line,"-->")
    #ssh.close ()


#username1 ="thh"
#host1 = "10.2.200.1"
#password1 = ""
#macaddress="54e1.ad67.720c"
#macaddress="3402.86b6.bfe3"
#interface ="GigabitEthernet2/0/29"
#command = "show run int GigabitEthernet2/0/29 "

#tho = runcommand (host1,username1,password1,command)

def runcommandpo (host1,username1,password1,command):
    host=host1
    username=username1
    password=password1
    #interface ="no value was found at central, please verify Device is connected to LAN NO WIRELESS"
    #interface = "1"
    ssh.connect(host1,username=username1,password=password1)
    stdin, stdout, stderr = ssh.exec_command (command)
    stdin.close()
    
    for line in stdout.readlines():
        #print (line)
        if "switchport mode trunk" in line:
            return 3
            
def runcommandwifi (host1,username1,password1,command):
    host=host1
    username=username1
    password=password1
    #interface ="no value was found at central, please verify Device is connected to LAN NO WIRELESS"
    #interface = "1"
    #ssh.connect(host1,username=username1,password=password1)
    try:
        ssh.connect("10.200.254.250",username=username1,password=password1)
    except TimeoutError:
        return (10,"Device timeout ERROR")
           
    #except paramiko.ssh_exception.SSHException:
    #    return (11,"SSH EXCEPTION ERROR")
            
    except ConnectionRefusedError:
        return (12,"End Device refuse to allow connection")     
    except paramiko.ssh_exception.BadHostKeyException:
        return (13,"BadHostKeyException")
    except paramiko.ssh_exception.AuthenticationException:
        return (14,"Wrong username or password")               
    except PermissionError: 
        return (15,"Unable to access script due to permision issue, please contact Tho.huynh@economical.com")                  
    except FileNotFoundError:
        return (16,"The portal is missing softwares")   
    except paramiko.ssh_exception.NoValidConnectionsError:
        return (17,"Invalid server IP")
    ####command = "show mac address-table address "+macaddress+ " | i "+macaddress
    #stdin, stdout, stderr = ssh.exec_command (command)
    #stdin.close()
    
    
    
    stdin, stdout, stderr = ssh.exec_command ("show netuser detail test")
    stdin.close()
    
    for line in stdout.readlines():
        print (line)
        