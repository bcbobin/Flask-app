import execute, main

def data():
	forminfo = {}
	forminfo['s_email'] = request.form['sponsoremail'].lower()
	forminfo['duration'] = request.form['length']

	if session['level'] == "full":
		#special check for ritm and allow full form creation
		hasritm = request.form['ritmcheck']
		if forminfo['length'] == "Custom":
			forminfo['length'] = request.form['enddate']
		
		forminfo['length'] = main.timeset(forminfo['length'])
		#check to see if they have an RITM number
		if hasritm == "No":
			forminfo['guestname'] = request.form['guestname']
			forminfo['guestemail'] = request.form['guestemail']
			forminfo['guestcompany'] = request.form['guestcompany']
			forminfo['guestphone'] = request.form['guestphone']
			forminfo['length'] = request.form['length']
			forminfo = missing(forminfo)
		else:
			data = main.record_retrieve(ritm_num, duration)
			if data['ritm_not_found'] == "true": 
				flash('Record could not be retrieved', 'danger')
			elif data['fail'] == "true":
				flash("RITM record returned unexpected value. Check RITM number!", 'danger')
			elif data['email_invalid'] == "true":
				flash("guest user email format incorrect, check RITM form!", 'danger')
			else:
				forminfo['guestname'] = data['guest_name']
				forminfo['guestemail'] = data['guest_email']
				forminfo['guestcompany'] = data['company']
				forminfo['guestphone'] = data['guest_phone']
				forminfo['length'] = str(data['duration_seconds'])
				forminfo = missing(forminfo)
		
		
	else:
		#regular auth process, aka no controller access
	
	guest_pass = main.pass_gen()
	
	
	
def controller(gemail, gname, gcompany, gphone, duration, sdept, semail, username, password, gpass, comments):
	counter = 0
	while(counter < 3):
		status = execute.execute(gemail, gname, gcompany, gphone, duration, sdept, semail, username, password, gpass , comments)
		if (status == 0):
			#flash inforamtion to the user to see the returned results of the script 
			passinfo =["Successful addition, guest user information: ", 
					"Username:      " +data['guest_email']+    '        Password: '+ guest_pass,
					'Guest Company: '+data['company']+    '     Guest Email: '+data['guest_email'] ,
					'Guest Phone:   '+data['guest_phone']+  '       Sponsor Email: '+s_email ,
					'Time Given:    '+ data['time_active'] + '      Expires on: '+  data['end_date'] ,
					]
			break
		else:
			return status
	if(counter == 3):
		return -4
	else:
		return passinfo
		
def missing(dict):
	for key, value in dict:
		if value == "":
			dict[key] == "N/A"
	return dict
