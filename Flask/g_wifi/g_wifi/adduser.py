import execute, main, g_wifi   
    
def reg_add(ritm, s_email, username, password, duration):
    duration = main.timeset(duration)               #get time to send to controller 
    #TODO- add auth step here for safety
    auth_check = main.authorize(username,password)       #in case initial auth times out
    if auth_check == -1:
        return -1       
    data = main.record_retrieve(ritm, duration)     #get form information
    #add error checks
    if data['ritm_not_found'] == "true":
        return -10
    elif data['fail'] == "true":
        return -11
    elif data['email_invalid'] == "true":
        return -12
    data = missing(data)                            #fill any empty fields with n/a to avoid whitespace issues
    guest_pass = main.pass_gen()                    #generate the guest's password
    #send the info to the controller 
    cont_response = controller(data['guest_email'],data['guest_name'],data['company'],data['guest_phone'], str(duration) ,data['s_dept'], s_email, username, password, guest_pass , data['details'], data['time_active'], data['end_date']  )
    if cont_response != -1 and cont_response != -2 and cont_response != -3 and cont_response != -4:
        main.update_records(ritm)                   #if no errors occured during the controller add, update the ritm to close 
    return cont_response
        
    
    
def controller(gemail, gname, gcompany, gphone, duration, sdept, s_email, username, password, gpass, comments, time_active, end_date):
    #print(gemail, gname, gcompany, gphone, duration, sdept, s_email, username, password, gpass, comments, time_active, end_date)
    counter = 0
    while(counter < 3):
        status = execute.execute(gemail, gname, gcompany, gphone, duration, sdept, s_email, username, password, gpass , comments)
        if status == -2:
            counter = 1 + counter
        elif (status == 0):
            #flash inforamtion to the user to see the returned results of the script 
            passinfo =("Successful addition, guest user information: </br>",
                    "Username:      " + gemail +    '        Password: '+ gpass + '</br>' ,
                    'Time Given:    '+ str(time_active) + '      Expires on: '+  str(end_date) + '</br>')
            break
        else:
            return status
    if(counter == 3):
        return -4
    else:
        return passinfo
        
def missing(dict):
    for key, value in dict.items():
        try:
            dict[key]= value.replace(" ", "")          #remove all whitespace for execute to function
        except (AttributeError, TypeError):                #skip the int of duration since it does not have strip()
            pass
        if dict[key] == "":                     #if variable is empty, fill it with n/a
            dict[key] = "N/A"
    return dict
