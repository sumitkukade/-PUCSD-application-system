from config_path import data
from mod_python import Session
def index(req):
    fp=open(data.path+"/project_data/stud_log.html","r");
    st=fp.read();
    session = Session.Session(req);
    session.cleanup()
    return st;
