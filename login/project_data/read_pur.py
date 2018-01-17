import MySQLdb
import datetime;
from mod_python import Session
from config_path import data
newflag=0
def index(req):
    info=req.form
    session = Session.Session(req);
    global Rollno
    try:
            Rollno=session['rno']
    except:
            return """<html>Session Expired<p><a href="../student_login.html"> LOGIN AGAIN</a></html>"""

    ip=session['ipaddr'];
    session.save()
    session.cleanup()
    flg=0
    try:
	edit=info['edit']
        
	edit=edit.split('Bonafide Certificate For')
	
	edit=edit[1].strip()
        
    except:
	edit='';
    try:
	e=info['e']
    	e=1;
    except:
	e=0
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    tabid="ApplicationRequests"

    ss=""" select max(appcnt) from applicationProcess.studentApplicationCount where rollNumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    count1=cursor.fetchall()
    count1= map(lambda x:x[0],count1);

    ss=""" select max(appcnt) from applicationProcess.studentApplicationCount where rollNumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    count2=cursor.fetchall()
    count2= map(lambda x:x[0],count2);
    



    ss="""select rollnumber from applicationProcess.studentApplicationQueue where rollnumber=%s and appId=%s;"""
    cursor.execute(ss,(Rollno,'APBN'))
    val1=cursor.fetchall()
    rn= map(lambda x:x[0],val1)
    fp=open(data.path+"/project_data/purpose.html","r")
    fp=fp.read()%(e,edit,edit,e)
    return fp


 
