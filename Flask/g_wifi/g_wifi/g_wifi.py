
import os, tempfile, datetime
from execute import execute
import util, main, cwlan, editNetmiko                                              #custom python files import
from flask import Flask, jsonify, request, render_template, flash, redirect, send_file, send_from_directory
import hashlib, netmiko, json


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "b'401b1fe929eda84ffba795ea55bc1a37c9ad103c4b6a95a01ba71d565497beec2d4848df47f07f0ca7ba37c93b49279561ab171df109255f4c5f376228a4d243'"

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

    #########Feb 22nd##########
#TODO - investigate logout button and fuctionality
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
    # if request.method == 'GET':
        # return redirect('/', code= 302)
  
    device1['username'] = request.form['login']
    device2['username'] = request.form['login']
    device1['password'] = request.form['password']
    device2['password'] = request.form['password']
    

    if(device1['username'] == "gwifi" and device1['password'] == "pass"):
        return render_template("gwifiindex.html", value="disabled")
    elif( device1['username'] == "cwlan" and device1['password'] == "pass"):
        return render_template("cwlanindex.html")
    elif( device1['username'] == "admin" and device1['password'] == "pass"):
        return render_template('indexboot.html')
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
                return render_template('indexboot.html', value="disabled")
            return render_template('indexboot.html', value="")



#comunicate with other script and pull post values 
@app.route('/new', methods=['POST'])
def data():
    #pull specific info from the html form by element name in html
    s_email = request.form['sponsoremail'].lower()
    #TODO - is an economical check required for sponser_email(possibly)
    ritm_num = request.form['ritm']
    duration = int(request.form['length'])
    print (duration)
    #check username and password for any specific bypasses and servicenow/controller authentication
    if(( device1['username'] == "wifiadmin" and device1['password'] == "4Wifi_Aut@mate") or ( device1['username'] == "servicedesk" and device1['password'] == "SDesk_Aut@mate")):
        auth = main.authorize(util.admin(), util.adminp())
    else:
        auth = main.authorize( device1['username'], device1['password'])   
    if auth == -1:
        flash("Authorization Failed, try again", 'danger')
    else:
        data = main.record_retrieve(ritm_num, duration)
       #if failed to retrieve record, specifiy why using the returned values as error flags
        if data['ritm_not_found'] == "true": 
            flash('Record could not be retrieved', 'danger')
        elif data['fail'] == "true":
            flash("RITM record returned unexpected value. Check RITM number!", 'danger')
        elif data['email_invalid'] == "true":
            flash("guest user email format incorrect, check RITM form!", 'danger')
        elif data['approval'] == "needed" and ( device1['username'] == "wifiadmin" or  device1['username'] == "servicedesk"):
            flash("time requested needs Networking Approval(7+ days)!", 'warning' )
        else:
            #if not errors continue to settiung up user
            guest_pass = main.pass_gen()
            counter = 0
            #use password that has contorller access if user does not 
            if(( device1['username'] == "wifiadmin" and device1['password'] == "4Wifi_Aut@mate") or ( device1['username'] == "servicedesk" and device1['password'] == "SDesk_Aut@mate")):
                device1['username'] = util.admin()
                device1['password'] = util.adminp()
            #try three times in case controller is busy (could take a while if needs all three tries (10 seconds))
            while(counter < 3):
                status = execute.execute(data['guest_email'], data['guest_name'], data['company'], data['guest_phone'], str(data['duration_seconds']), data['s_dept'], s_email, device1['username'],device1['password'],guest_pass,data['details'])
                if (status == -2):
                    counter = 1 + counter
                if (status == -1):                                          #checks for controller auth, kept in for safety 
                    flash("Invalid Username or Password", 'danger')   
                    break
                if (status == -3):
                    flash("Account already exists, search for " + data['guest_email'] + "to see account information", 'warning' )
                    break
                if (status == 0):
                    #flash inforamtion to the user to see the returned results of the script 
                    flash("Successful addition, guest user information: ", 'success')
                    flash("Username: " +data['guest_email']+ ' \n\n     Password: '+ guest_pass , 'success') 
                    flash(' \n\n Guest Company: '+data['company']+'     \n\n Guest Email: '+data['guest_email'] , 'success')
                    flash(' \n\n Guest Phone: '+data['guest_phone']+'    \n\n Sponsor Email: '+s_email , 'success')
                    flash(' \n\n Time Given: '+ data['time_active'] + '    \n\n Expires on: '+  data['end_date'] , 'success')
                    break
            if(counter == 3):
                flash("Controller is busy, try again in 5 minutes", 'warning')
            else:
                main.update_records(ritm_num)
    return redirect('/landing', code = 302)      #return back to main page after completion 
 

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
    

@app.route('/delete', methods=['POST'])
def delete():
    return

@app.route('/searchdata', methods=['GET', 'POST'])
def searchdata():
    username = request.form['search']
    output = json.dumps(editNetmiko.usersearch(username))
    if output == -1:
        flash("User could not be found", "danger")
    return render_template('indexboot.html', output = output)


#run the app on specified ip and port 
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.secret_key = "127067bbafca69f8603c507968adaa8729d4841da83a3ed1"