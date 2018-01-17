import MySQLdb
import datetime;
from mod_python import Session
from config_path import data
newflag=0
def index(req):
    session = Session.Session(req);
    info=req.form
    global Rollno
    try:
      	Rollno=session['rno']
    except:
         return """<html>Session Expired<p><a href="../student_login.html"> LOGIN AGAIN</a></html>"""
    

    

    try:
	edit=info['edit'];
	edit=1;
    except:
	edit=0;
    
    ip=session['ipaddr']
    session.save()
    session.cleanup()
    flg=0
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    tabid="ApplicationRequests"
    
    fp=open(data.path+"/project_data/bank_addr.html","r")
    fp=fp.read()%(edit)
    
    return fp
