#!/usr/bin/env python3.4
# Import modules for CGI handling 
import cgi, cgitb 
import sys , traceback
sys.path.insert(0, "/usr/local/lib/python3.4/site-packages/")


import edit

def controller1 (host,username,password,commandx,commandy):
    try:
        prod = edit.editconfig (host,username,password,commandx,commandy)
        
    except OSError as err:
        print("OS error: {0}".format(err))
        return 'failed'
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return 'failed'
    prod1= str (prod)
    #print ("prod1 value is ",prod1)
    return prod1
    
    
def controller2 (host,username,password,commandx,commandy):
    #print ("inside prod2")
    try:
        
        prod = edit.editconfig (host,username,password,commandx,commandy)
    except OSError as err:
        print("OS error: {0}".format(err))
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    prod2= str (prod)
    #print ("prod2 value is ",prod2)
    return prod2