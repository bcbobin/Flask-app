#!/usr/bin/env python3.4
# Import modules for CGI handling 
import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")
import os
import paramiko
import time
import logging
#LOG_FILENAME = 'example.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

#logging.debug('This message should go to the log file')
#remote_conn_pre=paramiko.SSHClient()
#remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def editconfig (host1,username1,password1,command,command1):
    #print ("command", command)
    
    
    try:
        ssh.connect(host1, username=username1,password=password1)
        #print ("testing ssh ")
    except OSError as err:
        ssh.close ()
        #print("OS error: {0}".format(err))
        #return 'failed'
    except:
        ssh.close ()
        #print("Unexpected error:", sys.exc_info()[0])
        return 'failed'
    
    
    #time.sleep (4)   
    #ssh.connect(host1, username=username1,password=password1)
    console = ssh.invoke_shell()
    output = console.recv(32768).decode('utf-8', 'ignore')
    #print (output)
    #print ("invoke shell")
    time.sleep(3)
    #print ("woke up after 3 seconds")
    console.keep_this = ssh
    #remote_conn_pre.connect(host1, username=username1,password=password1,look_for_keys=False, allow_agent=False)

    #remote_conn = remote_conn_pre.invoke_shell()
    #command = "config netuser add " + str (guestusername) +" "+ str (guestpassword) + " wlan 2 userType guest lifetime " + str(hours) + " description " + str (requestnumber) +"\n"
    try:
        console.send(username1+ "\n")
        #print ("insert username")
    except OSError as err:
        ssh.close ()
        #print("OS error: {0}".format(err))
        return 'failed'
    except:
        ssh.close ()
        print("Unexpected error:", sys.exc_info()[0])
        return 'failed'
    
    
    output = console.recv(32768)
    time.sleep(.1)
    test = str(output)
    #print ("password--------->>",output)

    try:
        console.send(password1+ "\n")
        #print ("insert password")
    except OSError as err:
        ssh.close ()
        #print("OS error: {0}".format(err))
        return 'password'
    except:
        ssh.close ()
        #print("Unexpected error:", sys.exc_info()[0])
        return 'password'
    #console.send(password1+ "\n")
    time.sleep(.1)
    output = console.recv(32768).decode('utf-8', 'ignore')
    while 'Password:' in output:
        console.send(password1+ "\n")
        time.sleep(.1)
        output = console.recv(32768).decode('utf-8', 'ignore')
        if 'User:' in output :
            console.send(username1+ "\n")
            time.sleep(.1)
        
        
    
        
    #test = str(output)
    #print ("after password",output)
    try:
        console.send(command1)
        #print ("Create user command1")
    except OSError as err:
        ssh.close ()
        #print("OS error: {0}".format(err))
        return 'failed'
    except:
        ssh.close ()
        #print("Unexpected error:", sys.exc_info()[0])
        return 'failed'
    #console.send(command1)
    time.sleep(.1)
    output = console.recv(32768).decode('utf-8', 'ignore')
    if 'exists' in output:
        #ssh.close ()
        return 'exists'
    #print (output)
    #test = str(output)
    
    #for i in output.readlines():
    #    print ("-->>",i)
    #print ("after command",output)
    try:
        console.send(command)
        #print ("Check for user command")
    except OSError as err:
        ssh.close ()
        #print("OS error: {0}".format(err))
        return 'failed'
    except:
        ssh.close ()
        #print("Unexpected error:", sys.exc_info()[0])
        return 'failed'
    #console.send(command)
    time.sleep(.1)
    output = console.recv(32768).decode('utf-8', 'ignore')
    #test = str(output)
    #print ("test",test)
    #ssh.close ()
    return output

    
    
    #remote_conn.send("config t\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())

    #remote_conn.send("interface "+interface+"\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())


    #remote_conn.send("description workstation-Asanka-Sibera-Datajack#2-285\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())


    #remote_conn.send("switchport access vlan 253\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())
    
    #remote_conn.send("end\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())

    #remote_conn.send("wr mem\n")
    #time.sleep(1)
    #output = remote_conn.recv(65535)
    #print (output.strip())
