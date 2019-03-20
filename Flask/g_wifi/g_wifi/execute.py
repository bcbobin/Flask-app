# coding: utf-8
#import main
# Import modules for CGI handling 

import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.6/site-packages/")

import paramiko
import time
import edit
import show
import runcommand
import emailout
import checkstatus
#import logging
#LOG_FILENAME = 'example.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

#logging.debug('This message should go to the log file')

#macaddress=input ("please provide MAC ADDRESS \n")
#deviceip = input ("please provide Device IP \n")
#host = input ("please provide the location of the device \n")
#tho = main.main1 (macaddress,deviceip)
#print ("running execute")
#deviceip = "10.2.71.37"
#host = "10.2.201.2"
#host = "10.2.200.1"
#macaddress="00b3.627f.786e"
#macaddress="0056.cd08.dfbd"

host1="10.200.254.250"
host2="10.208.254.250"
def execute(guestemail, guestfullname, guestcompany, guestphone, hours, sponsordepartment, sponsoremail,username1,password1,guestpassword,guestcomment):
    #guestemail = #_POST["guestemail"];
    #guestfullname = #_POST["guestfullname"];
    #guestcompany =  #_POST["guestcompany"];
    #guestphone = #_POST["guestphone"];
    #guestcomment = #_POST["guestcomment"];
    #HOURS = #_POST["HOURS"];
    #sponsordepartment = #_POST["sponsordepartment"];
    #sponsoremail = #_POST["sponsoremail"];
    #login = #_POST["login"];
    #password =  #_POST["password"];
    #$$$$$$$$$$$$$$$$$$$$
    # guestemail = sys.argv[1].lower()
    # guestfullname = sys.argv[2]
    # guestcompany = sys.argv[3]
    # guestphone = sys.argv[4]
    # hours = sys.argv[5]


    # sponsordepartment = sys.argv[6]
    # sponsoremail = sys.argv[7]
    # username1 = sys.argv[8]
    # password1 = sys.argv[9]
    # guestpassword = sys.argv[10]
    # guestcomment = sys.argv[11]
    #print ("printing sys value" )
    #for x in range(0, 12):
    #    print (x," ",sys.argv[x])

    #print ("sys.argv3",guestpassword)
    counter="false"
    b=0
    counterx=0
    #hours= "14400"
    guestusername = guestemail.lower()
    #guestpassword = "123"
    #username1 = login
    #password1 = password
    requestnumber = guestcomment
    #guestemail="testing123@lol.com"
    #guestcompany="blackberry"
    #guestphone="4167689507"
    #sponsoremail="tho.huynh@economical.com"
    thoemail="tho.huynh@economical.com"
    ntwemail="networkgroup@economical.com"
    deskside="deskside.support@economical.com"
    #&&&&&&&&&&&&&&&&&&

    command3="config netuser delete username "+ guestusername + "\n"
    command = "show netuser detail " + guestusername + "\n"
    #command = "show netuser summary \n"
    command1="config netuser add " + guestusername + " " + guestpassword +" "+" wlan 2 userType guest lifetime " + hours + " description "+ requestnumber +"\n"
    #command ="show netuser summary"
    #print ("the value for host is -------------------->",host,password,username,deviceip,macaddress)
    #print ("check value",hours,guestusername,guestpassword,username1,password1,requestnumber)
    commandx = 'show netuser summary' 
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #try:
    #    ssh.connect('10.2.201.2',username=username1,password=password1)
        
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])
    #stdin, stdout, stderr = ssh.exec_command (commandx)
    #stdin.close()
    #for line in stdout.readlines():
    #    print (line)
    prod1='failed'
    prod2='failed'
    deleteuser ='failed'
    counterprod1=0
    counterprod2=0
    counterprod3=0
    #while counter != "true":
        #try:
        #    prod = edit.editconfig (host1,username1,password1,command,command1)
            
        #except OSError as err:
        #    print("OS error: {0}".format(err))
        #    raise
        #except:
        #    print("Unexpected error:", sys.exc_info()[0])
        #    raise
        #prod1= str (prod)
        #try:
            
        #    prod = edit.editconfig (host2,username1,password1,command,command1)
        #except OSError as err:
        #    print("OS error: {0}".format(err))
        #   raise
        #except:
        #   print("Unexpected error:", sys.exc_info()[0])
        #   raise
        #prod2= str (prod)
    while prod1 == 'failed':
        prod1=checkstatus.controller1 (host2,username1,password1,command,command1)
        
        #print ("failed, counter will increase",counterprod1,prod1)
        counterprod1 += 1
        #print ("value for couter1",counterprod1)
        if "Lifetime" in prod1:
            #print ("calling Prod2")
            while prod2 =='failed':
                #print ("while loop prod2 just ran and its counter is ->>",counterprod2)
                prod2=checkstatus.controller2 (host1,username1,password1,command,command1)
                
                counterprod2 += 1
                #print ("value for couter2",counterprod2)
                if counterprod2==6 or 'exists' in prod1:
                    prod2='nothing'
                    #print ("inside the if statement for prod2")
                    while deleteuser =='failed' :
                        #print ("inside deleteuser")
                        deleteuser=checkstatus.controller1 (host1,username1,password1,command,command3)
                        if 'Username already exists' in prod2:
                            deleteuser=checkstatus.controller1 (host2,username1,password1,command,command3)
                        #print ("delete user",counterprod3)
                        counterprod3 += 1
                        #print ("value for couter3",counterprod3)
                        if counterprod3 == 6:
                            deleteuser='nothing'
        if counterprod1 == 6:
            prod1='nothing'
                
    #print ("exiting code for prod1",prod1)        
    if "Lifetime" in prod1 and "Lifetime" in prod2:
            
        prod1=prod1.replace (".","")
        prodx = prod1.strip ()
        p=prod1.split (' ')
        datax=len (p)
        p=[x for x in p if x]
        startdate= p[19] +" " + p [20]+" " +p[21]+" " +p[22]
        expireddate =p[25] +" " + p [26]+" " +p[27]+" " +p[28] +" " +p[29]+" " +p[30]+" " + p[31]
        #index1=0
        #for loop in p:
        #    print (p(0))
            #index1+=1
            
        #print ("User has been created ")
        commandx ='config paging disable'
        command = "show netuser detail " + guestusername + "\n"
        prod = show.editconfig (host1,username1,password1,commandx,command)
        intro='You are receiving this e-mail because a sponsor at Ecomomical has requested a guest wifi account on your behalf. Due to new Economical Security Requirements, all users must now have unique accounts in order to access the G-WLAN wireless Network. The username and password below has been created for you. Do not share this account information with anyone else on your team. '
        #prod2 = [x.replace("\r\n","") for x in prod2]
        intro0='\n\n How to access the BCRS Wireless Network \n'
        intro1='\n 1. Connect to G-WLAN. \n'
        intro2='\n 2. Open a web browser in I.E and surf to your favourite website or go to www.economical.com \n'
        intro3='\n 3. A login page will be loaded \n' 
        intro4='\n 4. Enter the credentials above into the login box on the page \n '
        intro5='\n Enjoy the Courtesy Internet Service '
        #startdate= p[24]+" " + p [25]+ " "+ p[26]
        #expireddate =p[30] +" " + p [31]+" " +p[33]+" " +p[34] +" " +p[35]+" " +p[36]+" " + p[37]
        #print ("value for startdate",startdate)
        #print ("Start Date: ",startdate)
        #print ("Expires in: ",expireddate)
        subjectx="ECONOMICAL Wireless Guest User Account Details : SSID G-WLAN "
        messagex= 'You are listed as the Sponsor for the following guest account. \n\n =============================================== \n\n Username:'+guestemail+' \n\n  Password:'+guestpassword+' \n\n Guest Company:'+guestcompany+'  \n\n Guest Email:'+guestemail+' \n\n Guest Phone: '+guestphone+' \n\n Sponsor Email:'+sponsoremail+' \n\n Start Date: '+ startdate + ' \n\n Expires in:'+  expireddate
        emailoutx =emailout.emailsponsor (subjectx, messagex,sponsoremail)
        messagex= 'Welcome to ECONOMICAL. \n\n =============================================== \n\n '+intro+'\n\n Username: '+guestemail+'  \n\n Password:'+guestpassword+'  \n\n Start Date: '+ startdate + ' \n Expires in:'+  expireddate + '\n\n' + intro1 + intro2+ intro3 +intro4 +intro5
        emailoutx =emailout.emailsponsor (subjectx, messagex,guestemail)
        subjectx="ECONOMICAL Wireless Guest User Account Details : SSID G-WLAN  "
        messagex ='INFO \n =============================================== \n\n Username:'+guestemail+' \n\n Guest Company:'+guestcompany+'  \n\n Guest Email:'+guestemail+' \n\n Guest Phone: '+guestphone+' \n\n Sponsor Email:'+sponsoremail+' \n\n Start Date: '+ startdate + ' \n Expires in: '+  expireddate + ' '
        #emailoutx =emailout.emailsponsor (subjectx, messagex,thoemail)
        subjectx="ECONOMICAL Wireless Guest User Account Details : SSID G-WLAN  "
        messagex ='INFO \n =============================================== \n\n Username:'+guestemail+' \n\n Guest Company:'+guestcompany+'  \n\n Guest Email:'+guestemail+' \n\n Guest Phone: '+guestphone+' \n\n Sponsor Email:'+sponsoremail+' \n\n Start Date: '+ startdate + ' \n Expires in: '+  expireddate + ' '
        #emailoutx =emailout.emailsponsor (subjectx, messagex,ntwemail)
        subjectx="ECONOMICAL Wireless Guest User Account Details : SSID G-WLAN  "
        messagex ='INFO \n =============================================== \n\n Username:'+guestemail+' \n\n Guest Company:'+guestcompany+'  \n\n Guest Email:'+guestemail+' \n\n Guest Phone: '+guestphone+' \n\n Sponsor Email:'+sponsoremail+' \n\n Start Date: '+ startdate + ' \n Expires in: '+  expireddate + ' '
        #emailoutx =emailout.emailsponsor (subjectx, messagex,deskside)
        
        
            #while  b < datax:
            #    print ("value for b",b)
            #    print (prod2[b])
            #    b +=1
        counter="true"   
        return 0 #("Successful, client info: ", prod)
    elif 'User:' in prod1:
            return -1 #("Invalid Username or Password")
            
    elif 'exists' in prod1:
            commandx ='config paging disable'
            command = "show netuser detail " + guestusername + "\n"
            #command ="show netuser summary"
            prod = show.editconfig (host1,username1,password1,commandx,command)
            return -3 #("The account is still active", str(prod))
            
    else :
        return -2 #("Request Timeout, Please try again")

    #prod1 = edit.editconfig (host1,username1,password1,guestusername,guestpassword,requestnumber,hours)
    #generatekey = runcommand.runcommandwifi (host1,username1,password1,command)
    #tho = main.getinfo (macaddress,deviceip,host)
    #if tho[0]==1:
    #    print ("\n\n\n")
    #    print ("1")# return to print (tho[1])
    #else :
    #    print ("\n\n\n")
    #    print ( "FAILED CHANGE ERROR CODE# ",tho[0]," Reason for Failure -->",tho[1])