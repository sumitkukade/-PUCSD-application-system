import MySQLdb
from mod_python import Session
from config_path import data
def index(req):

    req.content_type = 'text/html'
    #req.write('rollno: %s\n' % session['rno'])
    info = req.form
    rollno=info['rono']
    info1 = req.form
    appid=info1['apid']
    p=info1['prps']

    crpn=""
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="applicationProcess" )
    cursor = db.cursor()
    if appid=='APBN':
   	 q1 = """delete from applicationProcess.applicationRejectRemark where rollNumber=%s and appId=%s and applicationRemark=%s;"""
    	 cursor.execute(q1,(rollno,appid,p))
    	 db.commit()
    else:
	 q1 = """delete from applicationProcess.applicationRejectRemark where rollNumber=%s and appId=%s;"""
    	 cursor.execute(q1,(rollno,appid))
    	 db.commit()
    

    fp=open(data.path+"/project_data/autoclick5.html")
    fp=fp.read()   
    return fp

