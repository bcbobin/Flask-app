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
import update_rec


def read_excel(filename, username, dataToSendBack, userEmail, now):

  #try to find and read an excel file 
  while(True):
    try: 																				#control the columns pulled using usecols
      excel_file = pd.read_excel(filename, sheet_name=0, usecols= "A:J")				#issue found with using a sheetname for identification
      break																				#if sheet name does not match, the code will break and not terminate 
    except (FileNotFoundError):
      dataToSendBack["excel"] = "DNE"
      sys.stdout.flush()
      #message = email_user.email_message(dataToSendBack)
      #email_user.emailsponsor(message, userEmail, now)
      return -1

  try:
#read the excel and pull the data from columns named as such 
    #print(str(excel_file["Comments"]))
    #print(excel_file)
    asset_tag = excel_file['Asset Number']
    #drops any blank cell in the column so they do not get returned as nan, only for asset tags
    asset_tag.dropna(inplace = True)
    print(asset_tag.count())
    #sys.exit()
    #fill all NaN inputs with empty strings 
    excel_file.fillna("", inplace=True)
    serial_num = excel_file['Serial Number']
    #serial_num.dropna(inplace = True)
    state = excel_file['State']
    #state.dropna(inplace = True)
    assigned = excel_file['Assigned To']
    #assigned.fillna("")
    #print(assigned)
    stockroom = excel_file['Stockroom']
    #stockroom.dropna(inplace = True)
    #managed_by = excel_file['Managed By']
    #managed_by.dropna(inplace = True)
    attribute = excel_file['State Attribute']
    #attribute.dropna(inplace = True)
    comments = excel_file['Comments']
    #comments.dropna(inplace = True)
  except(KeyError):
    dataToSendBack["excel"] = "ImproperFormat"
    print(dataToSendBack)
    sys.stdout.flush()
    #message = email_user.email_message(dataToSendBack)
    #email_user.emailsponsor(message, userEmail, now)
    return -1
    
  run = True
  i = 0

  while (run):
  
    try:
      if(i == asset_tag.count()):
        dataToSendBack["numberOfUpdates"] = i - dataToSendBack["assetsFailed"]
        dataToSendBack["excel"] = "Finished"
        run = False
        break
      else: 
        atag = int(asset_tag[i])
    except (IndexError, KeyError):
      continue
  
    #retreive item sysid by sending a query
    #also change if tested outside of production 
    idurl = "https://economical.service-now.com/alm_hardware.do?JSONv2&sysparm_action=getKeys&sysparm_query=active=true^category=hardware^GOTOasset_tagLIKE" + str(atag) + "^ORDERBYasset_tag"
    req = urllib.request.Request(idurl)
    req = urllib.request.urlopen(idurl)
    data = req.read().decode()
    sysrecords = json.loads(data)
    #print(sysrecords)
    sysid = sysrecords.get("records")
    if (len(sysid) > 1):
      dataToSendBack["multiple_records"] = "True"
      dataToSendBack["assetsFailed"] += 1
      dataToSendBack["duplicate"] += str(atag) + " "
      i += 1
      continue
  
    #getting info from database as a dictionary using sysid
    #also change if tested outside of production 
    try:
      geturl = "https://economical.service-now.com/alm_hardware.do?JSONv2&sysparm_sys_id=" + str(sysid[0]) + "&displayvalue=true"
    except IndexError:
      i += 1
      dataToSendBack["notFound"] = "True"
      dataToSendBack["assetsFailed"] += 1
      dataToSendBack["DNE"] += str(atag) + " "
      continue

    formreq = urllib.request.Request(geturl)
    formreq = urllib.request.urlopen(geturl)
    str_raw = formreq.read().decode()
    raw = json.loads(str_raw)
    values = raw['records']
    #specify asset record for the first item returned by the query 
    info = values[0]
   
    #for reference of response
    #print(str(info))
      
    #data checking logic, look at index and try to read and compare, if DNE then just pass 
    new_data = {}
    
    try:  
      if(serial_num[i] != "" and serial_num[i] != info['serial_number']):
        new_data["serial_number"] = str(serial_num[i])
    except IndexError:
      pass
    #print("serial")
    try:
      if(state[i] != info["install_status"]):
        new_data["install_status"] = str(state[i])
    except IndexError:
      pass
    #print("state")
    try: 
      if(assigned[i] != info["assigned_to"]):
        new_data["assigned_to"] = str(assigned[i])
    except IndexError:
      pass
    #print("ass to")
    try: 
      if(stockroom[i] != info["stockroom"]):
        new_data["stockroom"] = str(stockroom[i])
    except IndexError:
      pass
    #print("stock")
    # try:
      # if(managed_by[i] != info["managed_by"]):
        # new_data["managed_by"] = str(managed_by[i])
    # except IndexError:
      # pass
    
    try:
      if(attribute[i] != info["u_state_attribute"]):
        new_data["u_state_attribute"] = str(attribute[i])
    except IndexError:
      pass
    #add the comments to the existing comments, if none exist, use generic update tag 
    #print("attribute")
    if(str(comments[i]) != ""):
      new_data["comments"] = info["comments"] + "\r\n"+ username.upper() + now.strftime(' %m/%d/%Y') + " - Updated record, comments provided: " + str(comments[i])
    else:
      new_data["comments"] = info["comments"] + "\r\n"+ username.upper() + now.strftime(' %m/%d/%Y') + " - Updated record, no comments provided"
    #print("try")
    i += 1
    update_rec.update_records(new_data, sysid, dataToSendBack)
    