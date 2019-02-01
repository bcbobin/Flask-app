
import os, tempfile, datetime
import main
import execute, util
import subprocess  #TODO(if importing other functions and not converting to python fully) - use to run php possibly 
from flask import Flask, jsonify, request, render_template, flash, redirect, send_file, send_from_directory
from passlib.hash import sha256_crypt #to be used for password encryption 
#from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = '▒R+▒4w▒▒Y}4*ҟ▒'        #use command to generate python -c 'import os; print(os.urandom(16))'
#UPLOAD_FOLDER = '/tmp'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')
    
#########Jan 25th##########
#TODO - add back dropdown for date, replace date logic (7 Days -> Friday next week iff Wednesday or after )
#TODO - lock site and authenticate (low prio)
#TODO - general error testing (bug hunt)

#comunicate with other script and pull post values 
@app.route('/new', methods=['POST'])
def data():
    s_username = request.form['login']
    s_password = request.form['password']
    s_email = request.form['sponsoremail'].lower()
    #TODO - is an economical check required for sponser_email
    ritm_num = request.form['ritm']
    duration = int(request.form['length'])
    print (duration)
    if((s_username == "wifiadmin" and s_password == "4Wifi_Aut@mate") or (s_username == "servicedesk" and s_password == "SDesk_Aut@mate")):
        auth = main.authorize(util.admin(), util.adminp())
    else:
        auth = main.authorize(s_username, s_password)   
    if auth == -1:
        flash("Authorization Failed, try again")
    else:
        data = main.record_retrieve(ritm_num, duration)
        if data['ritm_not_found'] == "true":
            flash('Record could not be retrieved')
        elif data['fail'] == "true":
            flash("RITM record returned unexpected value. Check RITM number!")
        elif data['email_invalid'] == "true":
            flash("guest user email format incorrect, check RITM form!")
        elif data['approval'] == "needed" and (s_username == "wifiadmin" or s_username == "servicedesk"):
            flash("time requested needs Networking Approval(7+ days)!" )
        else:
            guest_pass = main.pass_gen()
            counter = 0
            if((s_username == "wifiadmin" and s_password == "4Wifi_Aut@mate") or (s_username == "servicedesk" and s_password == "SDesk_Aut@mate")):
                s_username = util.admin()
                s_password = util.adminp()
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
    return redirect('/', code = 302)      
 
if __name__ == '__main__':
   app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))