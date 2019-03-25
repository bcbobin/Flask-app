# Created by Bogdan Bobin
# Last Updated August 6/18 
# Version 0.9.3
################################################################
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

#start is at the bottom of the file, since functions must be defined first 

#funtion that gets called to start the proccess and call all other functions
def run_update(username, password, filename, now ): 
  dataToSendBack = {}
  dataToSendBack["assetsFailed"] = 0
  dataToSendBack["failed"] = ""
  dataToSendBack["authorization"] = ""
  authorize(username, password, dataToSendBack)
  read_excel(filename, username, dataToSendBack, now)
  
  #for output of data to be read by node js
  dataToSendBack["finished"] = "True"
  dataToSendBack = json.dumps(dataToSendBack)
  print(dataToSendBack)
  sys.stdout.flush()
  
  
#dataToSendBack possible values 
#finished = True
#authorization = Failed/Passed
#updated = True
#excel = DNE/Finsished/ImproperFormat 
#multiple_records = True
#assetsFailed += #of failed assets
#failed = string of failed asset numbers
#numberOfUpdates = amount of assets updated
#notFound = True
  
def authorize(username, password, dataToSendBack):
  unauthorized = True
  
  while (unauthorized):

    #for authentication covering all future urllib.request uses
    url = "https://economical.service-now.com/api/now/v2/ui/table/alm_hardware"	
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    top_url = "https://economical.service-now.com/"
    password_mgr.add_password(None, top_url, username , password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    try:
      opener.open(url)
    except urllib.request.HTTPError as err:
      #stop code if auth fails
      if (err.code == 401):
        dataToSendBack['authorization'] = "Failed"
        dataToSendBack['finished'] = "True"
        dataToSendBack = json.dumps(dataToSendBack)
        print(dataToSendBack)
        sys.stdout.flush()
        sys.exit()
  
    unauthorized = False 
    urllib.request.install_opener(opener)
    dataToSendBack["authorization"] = "Passed"

def update_records(new, sysid, dataToSendBack):
	#updating records with html PUT request
	updateurl = 'https://economical.service-now.com/api/now/v1/table/alm_hardware/' + str(sysid[0])
	update = urllib.request.Request(updateurl, data=bytes(str(new), 'utf-8'), method='PUT')
	update.add_header('Content-Type', 'application/json;charset=utf-8')
	update.add_header('Accept', 'application/json')
	urllib.request.urlopen(update)
	dataToSendBack["updated"] = "True"

def read_excel(filename, username,dataToSendBack, now):

  
  while(True):
    try: 
      excel_file = pd.read_excel(filename, sheet_name='0')
      break
    except (FileNotFoundError):
      dataToSendBack["excel"] = "DNE"

  try:
#read the excel and pull the data from columns named as such 
    asset_tag = excel_file['Asset']
    #drops any blank cell in the column so they do not get returned as nan
    asset_tag.dropna(inplace = True)
    serial_num = excel_file['Serial']
    serial_num.dropna(inplace = True)
    state = excel_file['State']
    state.dropna(inplace = True)
    assigned = excel_file['Assigned To']
    assigned.dropna(inplace = True)
    stockroom = excel_file['Stockroom']
    stockroom.dropna(inplace = True)
    managed_by = excel_file['Managed By']
    managed_by.dropna(inplace = True)
    attribute = excel_file['State Attribute']
    attribute.dropna(inplace = True)
    comments = excel_file['Comments']
    comments.dropna(inplace = True)
  except(KeyError):
    dataToSendBack["excel"] = "ImproperFormat"
    dataToSendBack = json.dumps(dataToSendBack)
    print(dataToSendBack)
    sys.stdout.flush()
    sys.exit()
    
  run = True
  i = 0

  while (run):
    try:
      atag = int(asset_tag[i])
    except (IndexError, KeyError):
      dataToSendBack["numberOfUpdates"] = i - dataToSendBack["assetsFailed"]
      dataToSendBack["excel"] = "Finished"
      run = False
      break
  
  	#retreive item sysid by sending a query
    idurl = "https://economical.service-now.com/alm_hardware.do?JSONv2&sysparm_action=getKeys&sysparm_query=active=true^category=hardware^GOTOasset_tagLIKE" + str(atag) + "^ORDERBYasset_tag"
    req = urllib.request.Request(idurl)
    req = urllib.request.urlopen(idurl)
    data = req.read().decode()
    sysrecords = json.loads(data)
  	#print(sysrecords)
    sysid = sysrecords.get("records")
    if (len(sysid) > 1):
      dataToSendBack["multiple_records"] = "True"
      #print ("More than one asset contains this asset tag: "+ str(atag) +". Therfore it was skipped")
      dataToSendBack["assetsFailed"] += 1
      dataToSendBack["failed"] += str(atag) + " "
      i += 1
      continue
  
  	#getting info from database as a dictionary using sysid
    try:
  	  geturl = "https://economical.service-now.com/alm_hardware.do?JSONv2&sysparm_sys_id=" + str(sysid[0]) + "&displayvalue=true"
    except IndexError:
      i += 1
      dataToSendBack["notFound"] = "True"
      dataToSendBack["assetsFailed"] += 1
      #print( "asset record: "+ str(asset_tag[i]) + " not found" )
      dataToSendBack["failed"] += str(atag) + " "
      continue

    
  
    formreq = urllib.request.Request(geturl)
    formreq = urllib.request.urlopen(geturl)
    str_raw = formreq.read().decode()
    raw = json.loads(str_raw)
    values = raw['records']
    info = values[0]
  
  	#for reference of response
    #test = open("asset_data.txt", "w")
    #test.write(str(values))
    #test.close()
  
  	#data checking logic
    new_data = {}
    try:
      if(int(atag) != info['asset_tag']):
        new_data["asset_tag"] = str(atag)
    except IndexError:
      pass
  
    try:  
      if(serial_num[i] != info['serial_number']):
        new_data["serial_number"] = str(serial_num[i])
    except IndexError:
      pass
  
    try:
      if(state[i] != info["install_status"]):
        new_data["install_status"] = str(state[i])
    except IndexError:
      pass
  
    try: 
      if(assigned[i] != info["assigned_to"]):
        new_data["assigned_to"] = str(assigned[i])
    except IndexError:
      pass
  
    try: 
      if(stockroom[i] != info["stockroom"]):
        new_data["stockroom"] = str(stockroom[i])
    except IndexError:
      pass
    
    try:
      if(managed_by[i] != info["managed_by"]):
        new_data["managed_by"] = str(managed_by[i])
    except IndexError:
      pass
    
    try:
      if(attribute[i] != info["u_state_attribute"]):
        new_data["u_state_attribute"] = str(attribute[i])
    except IndexError:
      pass
    
    try:
      new_data["comments"] = info["comments"] + "\r\n"+ username.upper() + now.strftime(' %m/%d/%Y') + " - Updated record, comments provided: " + str(comments[i])
    except IndexError:
      new_data["comments"] = info["comments"] + "\r\n"+ username.upper() + now.strftime(' %m/%d/%Y') + " - Updated record, no comments provided"
      pass
  
    update_records(new_data, sysid, dataToSendBack)
    i += 1

now = datetime.datetime.now()
run_update(sys.argv[1],sys.argv[2],sys.argv[3], now)
