from config_path import data
from mod_python import Session

def index(req):
    fp=open(data.path+"/project_data/login.html","r");
    dt=fp.read()
    session = Session.Session(req);
    session.cleanup()
    session.clear()
    return """<html>%s</html>"""%(dt)
    
