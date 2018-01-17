import MySQLdb as db
import requests
import json
from random import randint
from passlib.apache import HtpasswdFile
import os.path
import os
import socket
from requests import get
import datetime
import dateparser


def handle_session(requset_for,site_name,roll_no):
		s = requests.Session()
		url = site_name
		if requset_for == "set":
				s.get(url+"/cookies/set/sessioncookie/"+roll_no)
				return s.cookies
		else:
				s.config['keep_alive'] = False




def add_user(username,password):
		cwd = os.path.abspath(__file__)[:-8]
		if os.path.exists(cwd+"login/.htpasswd") == False:
				ht = HtpasswdFile(cwd+"login/.htpasswd", new=True)
				result = ht.set_password(username, password)
				ht.save()
				return result
		else:
				ht = HtpasswdFile(cwd+"login/.htpasswd")
				result = ht.set_password(username, password)
				ht.save()
				if result == False:
						return True

def check_user_password_htpasswd(username,password):
		cwd = os.path.abspath(__file__)[:-8]
		ht = HtpasswdFile(cwd+"login/.htpasswd")
		return ht.check_password(username, password)

def staff_check_user_password_htpasswd(username,password):
		cwd = os.path.abspath(__file__)[:-8]
		ht = HtpasswdFile(cwd+"login/.staff.htpasswd")
		return ht.check_password(username, password)

def get_db_connection(database_name):
		database = db.connect('localhost','root','S',database_name)
		return database, database.cursor()

def login(data):
		data_dict = json.loads(data)
		site_name = data_dict["site-name"]
		roll_no = data_dict["rollno"]
		password = data_dict["password"]
		login_data = {'username': roll_no,'status': 'loggedIn'}
		query = "select password from userPassword where userId = '"+roll_no+"';"
		result = perform_sql_action("applicationProcess",query,'select')
		if False:# result == ():
				return "roll no. doesn't exist..! please signup to continue"
		elif True:# result[0][0] == password:
				if check_user_password_htpasswd(roll_no,password):
						## find current machine ip
						return "True"
				else:
						return "invalid password"

		else:
				return "invalid password"


## changing date to mysql date format (ex: YYYY-MM-DD)
def sql_date_format(date):
		date = dateparser.parse(date)
		date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
		return date


def signup(data):
	data_dict = json.loads(data)
	
	gender = data_dict["gender"]
	courseId = data_dict["courseId"]
	domicile = data_dict["domicile"]
	rollno = data_dict["rollno"]
	pin = data_dict["pin"]
	pwd = data_dict["pwd"]
	fname = data_dict["fname"]
	mname = data_dict["mname"]
	lname = data_dict["lname"]
	category = data_dict["category"]
	#dob = datetime.datetime.strptime(data_dict["dob"], "%d/%m/%Y").strftime("%Y-%m-%d")
	dob = data_dict["dob"]
	dob = sql_date_format(dob)
	mobile = data_dict["mobile"]
	email = data_dict["email"]
	semId = data_dict["semId"]
	address_line_1 = data_dict["address_line_1"]
	address_line_2 = data_dict["address_line_2"]
	address_line_3 = data_dict["address_line_3"]
	countryName = data_dict["countryName"]
	stateName = data_dict["stateName"]
	cityName = data_dict["cityName"]
	query = "insert into studentSignupDomain(rollNumber) values('"+rollno+"');"
	perform_sql_action("applicationProcess",query,"insert")


	query = "select signupId from studentSignupDomain where rollNumber = '" + rollno + "' order by signupId desc limit 1;"

	result = perform_sql_action("applicationProcess",query,"select")

	
	query = "insert into applicationProcess.studentDetailsDomain(rollNumber,courseId,semId,category,fname,mname,lname,email,dateOfBirth,contactNo,gender,domicile,adderessLine1,adderessLine2,adderessLine3,cityId,stateId,countryId,signupId,signupTime) values('"+ rollno +"','"+ courseId +"','" + semId +"','" + category + "','"+ fname +"','" + mname + "','" + lname +"','"+ email +"','" + dob + "','"+ mobile +"','" + gender + "','" + domicile + "','"+address_line_1 +"','"+address_line_2 +"','"+address_line_3 +"',(select cityId from applicationProcess.citiesDomain where cityName = '"+cityName+"' ),(select stateId from applicationProcess.statesDomain where stateName = '"+ stateName +"'),(select countryId from applicationProcess.countriesDomain where countryName = '"+ countryName +"'),'"+str(result[0][0])+"',NOW());"
	perform_sql_action("applicationProcess",query,"insert")

	add_user(rollno,pwd)

	if data_dict["internationalStudentFlag"] != "":
		visaNumber = data_dict["visaNumber"]
  		visaType = data_dict["visaType"]
  		visaDate = data_dict["visaDate"]
		visaDate = sql_date_format(visaDate)
  		visaExpiryDate = data_dict["visaExpiryDate"]
		visaExpiryDate = sql_date_format(visaExpiryDate)
  		passportNumber = data_dict["passportNumber"]
  		admissionDate = data_dict["admissionDate"]
		admissionDate = sql_date_format(admissionDate)
  		intCurrentAddressLine1 = data_dict["intCurrentAddressLine1"]
  		intCurrentAddressLine2 = data_dict["intCurrentAddressLine2"]
  		intCurrentAddressLine3 = data_dict["intCurrentAddressLine3"]
  		# concat address lines
  		intCurrentAddress = intCurrentAddressLine1 + intCurrentAddressLine2 + intCurrentAddressLine3

  		nationality = data_dict["nationality"]
  		passportIssuedOn = data_dict["passportIssuedOn"]
  		passportValidTill = data_dict["passportValidTill"]
  		query2 = "insert into applicationProcess.internationalStudentInformationDomain(rollNumber,nationality,studentAddrInCity,dateOfFirstAdmsn,passportNo,issuedOn,passportValidTill,visaNo,visaType,visaIssuedOn,visaValidTill,signupId,signupTime) values('"+rollno+"','"+nationality+"','"+intCurrentAddress+"','"+admissionDate+"','"+ passportNumber +"','"+ passportIssuedOn +"','"+ passportValidTill +"','"+visaNumber+"','"+visaType+"','"+ visaDate +"','"+visaExpiryDate+"','"+str(result[0][0])+"',NOW());"
  		perform_sql_action("applicationProcess",query2,"insert")

  	return "new_password,success"


def validate_pin(data):
		# this function is for forgot password
		data_dict = json.loads(data)
		pin = data_dict["pin"]
		roll_no = data_dict["roll_no"]
		new_pass = data_dict["new_password"]
		query = "SELECT userId FROM userIdDomain WHERE userId = '"+ roll_no +"';"
		result = perform_sql_action("applicationProcess",query,'select')
		if len(result) == 1:
				if is_valid_pin(data):
						add_user(roll_no,new_pass)
						query = "insert into inputRequests(requestTime,requestType,userId,tableId,params) values(NOW(),'insert','" + roll_no + "','userPassword','"+ new_pass +"');"
						ret = perform_sql_action("applicationProcess",query, 'insert')
						query = "delete from applicationProcess.applicationCodeBySystem where userId = " + roll_no + ";"
						perform_sql_action("applicationProcess",query, 'delete')

						return "new_password,success"
				else:
						return "pin,invalid," + pin
		else:
				return "rollno,invalid," + roll_no

def perform_sql_action(database_name,query, action):
		try:
				db_con, db_cur = get_db_connection(database_name)
				db_cur.execute(query)
				if(action == 'select'):
						result = db_cur.fetchall()
						db_cur.close()
						return result
				else:
						db_con.commit()
						db_con.close()
		except Exception as e:
				return "DatabaseError, "+str(e)




def is_valid_pin(data):
		data_dict = json.loads(data);
		roll_no  = data_dict["roll_no"]
		pin = data_dict["pin"];
		query = "select applicationCode from applicationProcess.applicationCodeBySystem where userId = '" + roll_no +"';"
		result = perform_sql_action("applicationProcess",query,"select")
		if result == ():
			return "PIN request NOT generated"

		if result[0][0] == pin:
				return True
		else:
				return "PIN not matched"


def forgot_password(data):
		data_dict = json.loads(data)
		roll_no = data_dict["roll_no"]
		random_number = str(randint(1000000, 9999999))
		query = "insert into inputRequests(requestTime,requestType,userId,tableId,params) values (NOW(),'insert','"+roll_no +"','applicationCodeBySystem', '"+ random_number+"')"
		result = perform_sql_action("userInputDatabase",query,"insert");
		return "True"


def get_student_reset_code(data):
		data_dict = json.loads(data)
		roll_no = data_dict["rollno"]
		query = "select applicationCode from applicationProcess.applicationCodeBySystem where userId = '" + roll_no + "';"
		result = perform_sql_action("applicationProcess",query,"select")
		if result == ():
				return "PIN request NOT generated by student " + roll_no
		return "reset pin is "+ str(result[0][0])

def signup_pin_generator(data):
		data_dict = json.loads(data)
		roll_no = data_dict["roll_no"]
		random_number = str(randint(1000000, 9999999))
		query = "select '"+ roll_no +"' in (select userId from applicationProcess.userIdDomain where userId = '"+ roll_no +"');"
		result = perform_sql_action("applicationProcess",query,"select");
		if int(result[0][0]) == 1:
				query = "insert into inputRequests(requestTime,requestType,userId,tableId,params) values (NOW(),'insert','"+roll_no +"','applicationCodeBySystem', '" + random_number +"')"
				result = perform_sql_action("userInputDatabase",query,"insert");
				return "True"
		else:
				return "False"

def old_staff_login(data):
		data_dict = json.loads(data)
		staff_username = data_dict["username"]
		staff_password = data_dict["password"]
		query = "select userId from applicationProcess.userPassword where userId = '"+staff_username+"'";
		result = perform_sql_action("applicationProcess",query,"select");
		try:
				if result[0][0] == staff_username:
						query = "select password from applicationProcess.userPassword where userId = '"+staff_username+"'";
						result = perform_sql_action("applicationProcess",query,"select");
						if result[0][0] == staff_password:
								return "True"
						else:
								return "False"
				else:
						return "False"
		except IndexError:
				return "user dosent signed in please check login details"


def staff_login(data):
		data_dict = json.loads(data)
		staff_username = data_dict["username"]
		staff_password = data_dict["password"]
		if staff_check_user_password_htpasswd(staff_username,staff_password):
				return "True"
		else:
				return "Invalid Login Details"



def get_country_names(data):

	data_dict = json.loads(data)

	if data_dict["requestFor"] == "country":
		query = "select countryName from applicationProcess.countriesDomain;"
		result = perform_sql_action("applicationProcess",query,"select")	
		finale_result = []
		for name in result:
			for nname in name:
				finale_result.append(name[0])

	if data_dict["requestFor"] == "state":
		countryName = data_dict["countryName"]
		query = "select stateName from applicationProcess.statesDomain where countryId = (select countryId from countriesDomain where countryName = '"+ countryName +"');"
		result = perform_sql_action("applicationProcess",query,"select")	
		finale_result = []
		for name in result:
			for nname in name:
				finale_result.append(name[0])

	if data_dict["requestFor"] == "city":
		stateName = data_dict["stateName"]
		query = "select cityName from applicationProcess.citiesDomain where stateId = (select stateId from statesDomain where stateName = '"+ stateName +"');"
		result = perform_sql_action("applicationProcess",query,"select")	
		finale_result = []
		for name in result:
			for nname in name:
				finale_result.append(name[0])

	
	return str(finale_result)[1:-1]




def get_student_filled_details(data):
	data_dict = json.loads(data)
	######################################## incomplete


	roll_no = data_dict["rollno"]
	query_courseId = "select courseId from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_semId = "select semId from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "';"
	query_category = "select category from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_fname = "select fname from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_mname = "select mname from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_lname = "select lname from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_email = "select email from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_dateOfBirth = "select dateOfBirth from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_contactNo = "select contactNo from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_gender = "select gender from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_domicile = "select domicile from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_adderessLine1 = "select adderessLine1 from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_adderessLine2 = "select adderessLine2 from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_adderessLine3 = "select adderessLine3 from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1;"
	query_cityId = "select cityName from applicationProcess.citiesDomain where cityId = (select cityId from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1);"
	query_stateId = "select stateName from applicationProcess.statesDomain where stateId = (select stateId from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1);"
	query_countryId = "select countryName from applicationProcess.countriesDomain where countryId = (select countryId from applicationProcess.studentDetailsDomain where rollNumber = '" + roll_no + "' order by signupId desc limit 1);"
	query_interNationalFlag = "select "+ roll_no +" in(select rollNumber from applicationProcess.internationalStudentInformationDomain);"

	courseId = perform_sql_action("applicationProcess",query_courseId,"select")
	semId = perform_sql_action("applicationProcess",query_semId,"select")
	category = perform_sql_action("applicationProcess",query_category,"select")
	fname = perform_sql_action("applicationProcess",query_fname,"select")
	mname = perform_sql_action("applicationProcess",query_mname,"select")
	lname = perform_sql_action("applicationProcess",query_lname,"select")
	email = perform_sql_action("applicationProcess",query_email,"select")
	dateOfBirth = perform_sql_action("applicationProcess",query_dateOfBirth,"select")
	contactNo = perform_sql_action("applicationProcess",query_contactNo,"select")
	gender = perform_sql_action("applicationProcess",query_gender,"select")
	domicile = perform_sql_action("applicationProcess",query_domicile,"select")
	adderessLine1 = perform_sql_action("applicationProcess",query_adderessLine1,"select")
	adderessLine2 = perform_sql_action("applicationProcess",query_adderessLine2,"select")
	adderessLine3 = perform_sql_action("applicationProcess",query_adderessLine3,"select")
	cityId = perform_sql_action("applicationProcess",query_cityId,"select")
	stateId = perform_sql_action("applicationProcess",query_stateId,"select")
	countryId = perform_sql_action("applicationProcess",query_countryId,"select")




	result = str(courseId) + str(semId) + str(category) + str(fname) + str(mname) + str(lname) + str(email) + str(dateOfBirth) + str(contactNo) + str(gender) + str(domicile) + str(adderessLine1) + str(adderessLine2) + str(adderessLine3) + str(cityId) + str(stateId) + str(countryId) 
	
	result = {}
	result["courseId"] = str(courseId[0][0])
	result["semId"] = str(semId[0][0])
	result["category"] = str(category[0][0])
	result["fname"] = str(fname[0][0])
	result["mname"] = str(mname[0][0])
	result["lname"] = str(lname[0][0])
	result["email"] = str(email[0][0])
	result["dateOfBirth"] = str(dateOfBirth[0][0])
	result["contactNo"] = str(contactNo[0][0])
	result["gender"] = str(gender[0][0])
	result["domicile"] = str(domicile[0][0])
	result["adderessLine1"] = str(adderessLine1[0][0])
	result["adderessLine2"] = str(adderessLine2[0][0])
	result["adderessLine3"] = str(adderessLine3[0][0])
	result["cityId"] = str(cityId[0][0])
	result["stateId"] = str(stateId[0][0])
	result["countryId"] = str(countryId[0][0])
	result["internationalStudentFlag"]
	result = json.dumps(result)
	return result





def change_student_filled_details(data):
	######################################## incomplete
	data_dict = json.loads(data)

	gender = data_dict["gender"]
	courseId = data_dict["courseId"]
	domicile = data_dict["domicile"]
	rollno = data_dict["rollno"]
	fname = data_dict["fname"]
	mname = data_dict["mname"]
	lname = data_dict["lname"]
	category = data_dict["category"]
	#dob = datetime.datetime.strptime(data_dict["dob"], "%d/%m/%Y").strftime("%Y-%m-%d")
	dob = data_dict["dob"]
	mobile = data_dict["mobile"]
	email = data_dict["email"]
	semId = data_dict["semId"]
	address_line_1 = data_dict["address_line_1"] 
	address_line_2 = data_dict["address_line_2"]
	address_line_3 = data_dict["address_line_3"]
	countryName = data_dict["countryName"]
	stateName = data_dict["stateName"]
	cityName = data_dict["cityName"]


	query = "insert into studentSignupDomain(rollNumber) values('"+rollno+"');"
	perform_sql_action("applicationProcess",query,"insert")

	query = "select signupId from studentSignupDomain where rollNumber = '" + rollno + "' order by signupId desc limit 1;"

	result = perform_sql_action("applicationProcess",query,"select")

	
	query = "insert into applicationProcess.studentDetailsDomain(rollNumber,courseId,semId,category,fname,mname,lname,email,dateOfBirth,contactNo,gender,domicile,adderessLine1,adderessLine2,adderessLine3,cityId,stateId,countryId,signupId,signupTime) values('"+ rollno +"','"+ courseId +"','" + semId +"','" + category + "','"+ fname +"','" + mname + "','" + lname +"','"+ email +"','" + dob + "','"+ mobile +"','" + gender + "','" + domicile + "','"+address_line_1 +"','"+address_line_2 +"','"+address_line_3 +"',(select cityId from applicationProcess.citiesDomain where cityName = '"+cityName+"' ),(select stateId from applicationProcess.statesDomain where stateName = '"+ stateName +"'),(select countryId from applicationProcess.countriesDomain where countryName = '"+ countryName +"'),'"+str(result[0][0])+"',NOW());"
	perform_sql_action("applicationProcess",query,"insert")

	return "true"

