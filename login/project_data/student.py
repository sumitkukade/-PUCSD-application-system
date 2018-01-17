import MySQLdb
import time
from mod_python import Session
from config_path import data
def index(req):
    session = Session.Session(req)
    info = req.form
    session.cleanup()
    rollno=info['number']
    session['ipaddr']="192.1.114.80"	
    session['rno']=rollno
    session.save()
    session.cleanup()
    req.content_type = 'text/html'
    fp=open(data.path+"/project_data/autoclick2.html");
    fp=fp.read();
    return fp
