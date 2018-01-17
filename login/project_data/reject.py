from config_path import data
import MySQLdb
import time;
import refno
from mod_python import Session
from config_path import data
import student
def index(req):
   session = Session.Session(req);
   try:
       sname=session['sno'];
   except:
           return """<html>Session Expired<p><a href="../staff_log.html"> LOGIN AGAIN</a></html>"""

   ip=session['ipaddr']
   session.save()
   session.cleanup() 
   info=req.form
   app=info['docm']
   Rollno=info['rono']
   db = MySQLdb.connect(
   host="localhost",
   user=data.mysql_user,
   passwd=data.mysql_pswd,
   db="userInputDatabase" )
   cursor = db.cursor()
   appid=["APBN","APFS","APIB","APND"]
   arrayid=["Bonafide Certificate,apply for Bonafide Certificate","Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]
   if app=='APBN':
	   
	   p=info['prps']
	   ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s and applicationPurpose=%s;"""
	   cursor.execute(ss2,(Rollno,app,p))
	   valq=cursor.fetchall()
	   statess=valq[len(valq)-1]
	   arrayid=["Bonafide Certificate,%s"%(p),"Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]

		
	   if statess==('ApplicationSubmitted', 'RequestArrivedInOffice'):
	
        	ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",RequestArrivedInOffice,ApplicationRejectedByOffice,"%s","%s);"""
        	cursor.execute(ss,(sname,ip,app,Rollno,arrayid[appid.index(app)]))
       	        db.commit()  
  	   else:
   		ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",ApplicationModification,ApplicationRejectedByOffice,"%s","%s);"""
        
                cursor.execute(ss,(sname,ip,app,Rollno,arrayid[appid.index(app)]))
                db.commit()

   else:	   
   	ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s;"""
   	cursor.execute(ss2,(Rollno,app))
   	valq=cursor.fetchall()
              
   	statess=valq[len(valq)-1]
	
   
   	if statess==('ApplicationSubmitted', 'RequestArrivedInOffice'):
	
        	ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",RequestArrivedInOffice,ApplicationRejectedByOffice,"%s","%s);"""
        	cursor.execute(ss,(sname,ip,app,Rollno,arrayid[appid.index(app)]))
       		db.commit()  
   	else:
   		ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",ApplicationModification,ApplicationRejectedByOffice,"%s","%s);"""
        
        	cursor.execute(ss,(sname,ip,app,Rollno,arrayid[appid.index(app)]))
        	db.commit()
   fp=open(data.path+"/project_data/autoclick.html")
   fp=fp.read()   
   return fp
