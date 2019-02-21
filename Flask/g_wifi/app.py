
import os, tempfile, datetime
import execute, util, main, cwlan                                              #custom python files import
from flask import Flask, jsonify, request, render_template, flash, redirect, send_file, send_from_directory
import hashlib, netmiko


app = Flask(__name__, static_folder='static', static_url_path='/static')

    #########Feb 21th##########
#TODO - have different types of flash message colors to indicate success or failiure  
#TODO - restructure authentication
#TODO - intergrate database into site
#TODO - convert all tabs/forms to work without php
#TODO - general error testing (bug hunt)

#login page for authentication 
@app.route('/')
def home():
    return render_template('login.html')
       
#checks user input and gives entrace to main site (will be using a database to check or servicenow)
@app.route('/landing', methods=['GET','POST'])
def permission():
###############################################
#for controller auth -  note, two controllers that need to be pinged when updates are made IPs: 10.200.254.250 and 10.208.254.250
#device1 = {
#   'device_type': 'cisco_wlc', 
#   'ip': '10.200.254.250',
#   'username': '',                                         # use the provided password and user
#   'password': '',
#}

#device2 = {
#   'device_type': 'cisco_wlc', 
#   'ip': '10.208.254.250',
#   'username': '',                                         
#   'password': '',
#}
#try: 
#   connect = netmiko.ConnectHandler(**device1)
#except (ValueError):
#   try: 
#       connect = netmiko.ConnectHandler(**device2)
#   except (ValueError):
#       flash("User does not have controller access")
#       return
################################################

    #deny access if method is GET, should be attempting a post with credentials only
    if request.method == 'GET':
        return redirect('/', code= 302)
  
    s_username = request.form['login']
    s_password = request.form['password']
    
    #will move service now authentication here, password and username will not leave this method for security
    if(s_username == "gwifi" and s_password == "pass"):
        return render_template("gwifiindex.html")
    elif(s_username == "cwlan" and s_password == "pass"):
        return render_template("cwlanindex.html")
    elif(s_username == "admin" and s_password == "pass"):
        return render_template('indexboot.html')
    else:
        auth = main.authorize(s_username, s_password) 
        if auth == -1:
            flash("Authorization Failed, try again")
            return redirect('/', code = 302)
        else:
            return render_template('indexboot.html')



#comunicate with other script and pull post values 
@app.route('/new', methods=['POST'])
def data():
    #pull specific info from the html form by element name in html
    s_email = request.form['sponsoremail'].lower()
    print(s_username)
    print(s_password)
    #TODO - is an economical check required for sponser_email(possibly)
    ritm_num = request.form['ritm']
    duration = int(request.form['length'])
    print (duration)
    #check username and password for any specific bypasses and servicenow/controller authentication
    if((s_username == "wifiadmin" and s_password == "4Wifi_Aut@mate") or (s_username == "servicedesk" and s_password == "SDesk_Aut@mate")):
        auth = main.authorize(util.admin(), util.adminp())
    else:
        auth = main.authorize(s_username, s_password)   
    if auth == -1:
        flash("Authorization Failed, try again")
    else:
        data = main.record_retrieve(ritm_num, duration)
       #if failed to retrieve record, specifiy why using the returned values as error flags
        if data['ritm_not_found'] == "true": 
            flash('Record could not be retrieved')
        elif data['fail'] == "true":
            flash("RITM record returned unexpected value. Check RITM number!")
        elif data['email_invalid'] == "true":
            flash("guest user email format incorrect, check RITM form!")
        elif data['approval'] == "needed" and (s_username == "wifiadmin" or s_username == "servicedesk"):
            flash("time requested needs Networking Approval(7+ days)!" )
        else:
            #if not errors continue to settiung up user
            guest_pass = main.pass_gen()
            counter = 0
            #use password that has contorller access if user does not 
            if((s_username == "wifiadmin" and s_password == "4Wifi_Aut@mate") or (s_username == "servicedesk" and s_password == "SDesk_Aut@mate")):
                s_username = util.admin()
                s_password = util.adminp()
            #try three times in case controller is busy (could take a while if needs all three tries (10 seconds))
            while(counter < 3):
                status = execute.execute(data['guest_email'], data['guest_name'], data['company'], data['guest_phone'], str(data['duration_seconds']), data['s_dept'], s_email,s_username,s_password,guest_pass,data['details'])
                if (status == -2):
                    counter = 1 + counter
                if (status == -1):                                          #checks for controller auth, kept in for safety 
                    flash("Invalid Username or Password")   
                    break
                if (status == -3):
                    flash("Account already exists, search for " + data['guest_email'] + "to see account information" )
                    break
                if (status == 0):
                    #flash inforamtion to the user to see the returned results of the script 
                    flash("Successful addition, guest user information: ")
                    flash("Username: " +data['guest_email']+ ' \n\n     Password: '+ guest_pass) 
                    flash(' \n\n Guest Company: '+data['company']+'     \n\n Guest Email: '+data['guest_email'])
                    flash(' \n\n Guest Phone: '+data['guest_phone']+'    \n\n Sponsor Email: '+s_email)
                    flash(' \n\n Time Given: '+ data['time_active'] + '    \n\n Expires on: '+  data['end_date'])
                    break
            if(counter == 3):
                flash("Controller is busy, try again in 5 minutes")
            else:
                main.update_records(ritm_num)
    return redirect('/', code = 302)      #return back to main page after completion 
 

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
	
	add = cwlan.add_user(cont1, cont2, mac, startdate, enddate)
	
	if add == -1:
		flash('User could not be added, incorrect MAC address')
	elif add = 1:
		flash('User already exists!')
	else:
		flash('User has been successfully added!')
		
    return redirect('/landing', code = 302)      #return back to main page after completion 
    

@app.route('/delete', methods=['POST'])
def delete():
    return

@app.route('/search', methods=['POST'])
def search():
    return




#run the app on specified ip and port 
if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))