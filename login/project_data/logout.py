import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session
def index(req):
    session = Session.Session(req);
    session.delete()
    
    fp=open(data.path+"/project_data/auto6.html")
    fp=fp.read()   
    return fp
    
