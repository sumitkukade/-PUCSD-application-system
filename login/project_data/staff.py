import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session   
def index(req):
    info=req.form;
    session = Session.Session(req)
    session.cleanup()
    sname=info['number']	
    session['sno']=sname
    session['cnt']=0;
    session['loop']=0
    session['ipaddr']='192.1.114.80'
    session.save()
    session.cleanup()
    fp=open(data.path+"/project_data/autoclick.html");
    fp=fp.read();
    return fp
   
