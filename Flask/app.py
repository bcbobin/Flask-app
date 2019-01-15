import os, tempfile, datetime
import script_run
from flask import Flask, jsonify, request, render_template, flash, redirect, send_file
#from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = '▒JO▒(▒)ty▒+▒!'
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#socketio = SocketIO(app)


dataToSendBack = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data', methods=['POST'])
def data():
    username = request.form['user_name']
    password = request.form['user_password']
    #email = request.form['user_email']
    file = request.files['fileUpload']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
    dataToSendBack = script_run.run_update(username, password, app.config['UPLOAD_FOLDER'] + '/' + file.filename, "empty")
    #print(app.config['UPLOAD_FOLDER'])
    if(dataToSendBack['authorization'] == 'Failed'):
        flash('Authorization Failed, please try again')
    if(dataToSendBack['excel'] == 'ImproperFormat'):
        flash('Excel file does not contain expected material, please check excel template')
    if(dataToSendBack['finished'] == 'True' and dataToSendBack['authorization'] == 'Passed' and dataToSendBack['excel'] == 'Finished' ):
        #flash('Script exectution complete')
        handle, path = tempfile.mkstemp(prefix='Results_')
        try:
            with os.fdopen(handle, 'w') as tmp:
                tmp.write("Script has successfully finshed, " + str(dataToSendBack["numberOfUpdates"]) + " assets have been updated. " + str(dataToSendBack["assetsFailed"]) + " assets could not be updated. ")
                if (dataToSendBack["notFound"] == "True"):
                    tmp.write("\nThe following asset numbers could not be found: \n" + str(dataToSendBack["DNE"]))
                if (dataToSendBack["multiple_records"] == "True" ):
                   tmp.write("\nThe following asset numbers had multiple entries: \n" + str(dataToSendBack["duplicate"]))
        finally:
            flash('Script exectution complete')
            return send_file(path, as_attachment = True, mimetype = "text/plain", attachment_filename = "Results" + datetime.datetime.now().strftime('%c')+ ".txt")
    
    
    
        
    return redirect('/', code = 302)
   #return jsonify({'username': username, 'pass': password, 'email': email, 'filename': path + "/" + filename.filename})        #will be made into redirect back to '/'
    #comunicate with other script and pull post values 

@app.route('/landing')              #can fix some issues when deployed on apache since template render no longer needed. Can just use redirects with html loaded using apache by default
def landing():
    handle, path = tempfile.mkstemp(prefix='Results_')
    try:
        with os.fdopen(handle, 'w') as tmp:
            tmp.write("Script has successfully finshed, " + str(dataToSendBack["numberOfUpdates"]) + " assets have been updated. " + str(dataToSendBack["assetsFailed"]) + " assets could not be updated. ")
            if (dataToSendBack["notFound"] == "True"):
                tmp.write("\nThe following asset numbers could not be found: \n" + str(dataToSendBack["DNE"]))
            if (dataToSendBack["multiple_records"] == "True" ):
               tmp.write("\nThe following asset numbers had multiple entries: \n" + str(dataToSendBack["duplicate"]))
    finally:
        return send_file(path, as_attachment = True, mimetype = "text/plain", attachment_filename = "Results" + datetime.datetime.now().strftime('%c')+ ".txt")
            

if __name__ == '__main__':
   app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))