from config_path import data
from mod_python import Session 
def index(req):
    fp=open(data.path+"/project_data/staff_log.html","r");
    st=fp.read();
    session = Session.Session(req);
    session.delete()
    session.cleanup()
    return st;
