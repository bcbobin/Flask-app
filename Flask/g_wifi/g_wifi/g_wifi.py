# Created by Bogdan Bobin
# Last Updated March 8/19
# Version 0.9.1
################################################################

import os, tempfile, datetime
import util, main, cwlan, editNetmiko, execute, adduser                                          #custom python files import
from flask import Flask, session, jsonify, request, render_template, flash, redirect, send_file, send_from_directory
import hashlib, netmiko, json


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "b'401b1fe929eda84ffba795ea55bc1a37c9ad103c4b6a95a01ba71d565497beec2d4848df47f07f0ca7ba37c93b49279561ab171df109255f4c5f376228a4d243'"

###############################################
# note, two controllers that need to be pinged when updates are made IPs: 10.200.254.250 and 10.208.254.250
###############################################

device1 = {
   'device_type': 'cisco_wlc', 
   'ip': '10.200.254.250',
   'username': '',                                         # use the provided password and user
   'password': '',
}

device2 = {
   'device_type': 'cisco_wlc', 
   'ip': '10.208.254.250',
   'username': '',                                         
   'password': '',
}

#access levels
guestwifi ={
    'value': "hidden",
    'cwlandisplay': "none",
    'wifidisplay': "",
    'vlandisplay': "none",
    'showvlan': "none",
    'showwifi': "block",
    'showcwlan': "none",
    'ritm': 'none',
}

cwlan = {
    'value': "hidden",
    'cwlandisplay': "",
    'wifidisplay': "none",
    'vlandisplay': "none",
    'showvlan': "none",
    'showwifi': "none",
    'showcwlan': "block",
    'ritm': 'none',
}

full = {
    'value': "",
    'cwlandisplay': "",
    'wifidisplay': "",
    'vlandisplay': "",
    'showvlan': "none",
    'showwifi': "block",
    'showcwlan': "none",
    'ritm': 'block',
}

    #########March 8th##########
#TODO - Search Table:
#TODO - add delete and search buttons to the table as well as sort options for the columns (Ben)
#TODO - shrink size of table text (Ben)

#TODO - Form:

#TODO - Functionality:
#TODO - make and test all button submits and test functionality of scripts 
#TODO - investigate logout button and fuctionality (BB)
#TODO - intergrate database into site (BB/Tho)
#TODO - convert all tabs/forms to work without php (BB)


#login page for authentication 
@app.route('/')
def home():
    return render_template('login.html')
#checks user input and gives entrace to main site (will be using a database to check or servicenow)
@app.route('/landing', methods=['GET','POST'])
def permission():

    #block get requests, might be needed for security reasons
    # if request.method == 'GET':
        # return redirect('/', code= 302)
  
    device1['username'] = request.form['login']
    device2['username'] = request.form['login']
    device1['password'] = request.form['password']
    device2['password'] = request.form['password']
    
#display vars control which buttons are visable to user, value hides select values when access is not full 
    if(( device1['username'] == "wifiadmin" and device1['password'] == "4Wifi_Aut@mate") or ( device1['username'] == "servicedesk" and device1['password'] == "SDesk_Aut@mate")):
        session['level'] = guestwifi
        return render_template("indexboot.html", vars = session['level'])
    if(device1['username'] == "gwifi" and device1['password'] == "pass"):
        session['level'] = guestwifi
        return render_template("indexboot.html", vars = session['level'])
    elif( device1['username'] == "cwlan" and device1['password'] == "pass"):
        session['level'] = cwlan
        return render_template("indexboot.html", vars = session['level'])
    elif( device1['username'] == "admin" and device1['password'] == "pass"):
        session['level'] = full
        return render_template("indexboot.html", vars = session['level'])
    else:
        auth = main.authorize( device1['username'], device1['password']) 
        if auth == -1:
            flash("Authorization Failed, try again", 'danger')
            return redirect('/', code = 302)
        else:
            try:                                                            #check if user exits on the controllers, slows down login
               connect = netmiko.ConnectHandler(**device1)                  #to speed up, only check one controller or have it converted to database check
            except (ValueError):
               # try: 
                   # connect = netmiko.ConnectHandler(**device2)
               # except (ValueError):
                session['level'] = guestwifi
                return render_template("indexboot.html", vars = session['level'])
            session['level'] = full
            return render_template("indexboot.html", vars = session['level'])



#comunicate with other script and pull post values 
@app.route('/new', methods=['POST'])
def data():
    #pull specific info from the html form by element name in html
    s_email = request.form['sponsoremail'].lower()  #TODO - is an economical check required for sponser_email(possibly)
    ritm_num = request.form['ritm']
    duration = request.form['length']

    #when custom is selected, fetch the end date
    if (duration == "Custom"):               
        duration = request.form['enddate']   
    #check username and password for any specific bypasses and servicenow/controller authentication
    if session['level'] == full:
        hasritm = request.form['ritmcheck']
        if hasritm == "No":
            forminfo = {}
            forminfo['guestname'] = request.form['guestname']
            forminfo['guestemail'] = request.form['guestemail']
            forminfo['guestcompany'] = request.form['guestcompany']
            forminfo['guestphone'] = request.form['guestphone']
            forminfo = adduser.missing(forminfo)                        #pull all the form info and check for blanks
            duration = main.timeset(duration)                           #convert time inputted to seconds 
            g_pass = main.pass_gen()                                    #gen guest pass
            #send data directly to controller as there are no records to pull or update 
            adduser.controller(forminfo['guestemail'], forminfo['guestname'], forminfo['guestcompany'], forminfo['guestphone'], str(duration), "Network", s_email, device1['username'], device1['password'], g_pass, "N/A")
        else:
            result = adduser.reg_add(ritm_num, s_email, device1['username'], device1['password'], duration)
    else:
        if(device1['username'] == "wifiadmin" or device1['username'] == "servicedesk"):
            device1['username'] = util.admin()
            device1['password'] = util.adminp()
            device2['username'] = util.admin()
            device2['password'] = util.adminp()
            
        result = adduser.reg_add(ritm_num, s_email, device1['username'], device1['password'], duration)
    if (result == -10):                                     #could not match an active record to the RITM provided 
        flash("Record could not be found!" , "danger")
    elif (result == -11):                                   #this is bad, means format has changed 
        flash("Information could not be pulled from the RITM", "danger")
    elif (result == -12):
        flash("The email entered on the RITM is invalid, please give a valid email on the RITM form", "danger")     #email given on RITM is not an acutal email
    elif (result == -1):                                          #checks for controller auth, kept in for safety 
        flash("Invalid Username or Password", 'danger')      
    elif(result == -2):                                         #probably not need but added for safety  
        flash("Request Timeout, Please try again", 'warning')          
    elif (result == -3):
        flash("Account already exists, search for user to see account information", 'warning' )
    elif(result == -4):                                     #timeout, controller is busy or other issue
        flash("Controller is busy, try again in 5 minutes", 'warning')
    else:
        #flash inforamtion to the user to see the returned results of the script 
        flash[:result] = passinfo.join("<br/>").html_safe
            
    return render_template("indexboot.html", vars = session['level'])      #return back to main page after completion 
 

@app.route('/add', methods=['POST'])
def add():
    mac_addr = request.form['MAC']
    spon_name = request.form['spon_name']
    spon_email = request.form['spon_email']
    start_date = request.form['startdate']
    end_date = request.form['enddate']
    user_name = request.form['users_name']
    user_email = request.form['user_email']
    user_company = request.form['user_company'] 
    
    add = cwlan.add_user(device1, device2, mac_addr, start_date, end_date)
    
    if add == -1:
        flash('User could not be added, incorrect MAC address', 'danger')
    elif add == 1:
        flash('User already exists!', 'warning')
    else:
        flash('User has been successfully added!', 'success')
        
        
    return redirect('/landing', code = 302)      #return back to main page after completion 
    

@app.route('/edit', methods=['POST'])
def delete():
    extend = request.form['extendSelect']
    user = request.form['radioButtons']
    if extend == 0:
        #delete function
        result = editNetmiko.deleteuser(user)
        if result == -1:
            flash("Something went wrong, please try again. If it persists, contact the Network Team", "danger")
        if result == 1:
            flash("User already did not exist!", "warning")
        else:
            flash("User was successfully deleted!", "success")
    else: 
        #extend function
        result = editNetmiko.extenduser(user, extend)
        if result == -1:
            flash("Could not find the user to extend!", "danger")
        else:
            flash("User was successfully extended", "success")
    return render_templete('indexboot.html', vars = session['level'])

@app.route('/searchdata', methods=['GET', 'POST'])
def searchdata():
    username = request.form['search']
    username.replace(" ", "")
    output = json.dumps(editNetmiko.usersearch(username))
    if output == -1:
        flash("User could not be found", "danger")
    return render_template('indexboot.html', vars = session['level'], output = output, input = username)


#run the app on specified ip and port 
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.secret_key = "127067bbafca69f8603c507968adaa8729d4841da83a3ed1"