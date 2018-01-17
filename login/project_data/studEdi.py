import MySQLdb
from mod_python import Session
from config_path import data
def index(req): 
         doc=''
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         states=('')
         info=req.form
         rollno=info['rono']
         info1=req.form 
         docc=info['docm'] 
         req.content_type='text/html'
         ss="""select Status from StudentStatus where RollNo=%s and Document=%s;"""
         cursor.execute(ss,(rollno,docc))
         val=cursor.fetchall()
         val= map(lambda x:x[0],val)
         
         
         if docc=='Bonafide Certificate':
                doc+="""<html>Click On Button To Edit!!!<head><body><form value="form" action="read_pur.py" method="post"><input type=\"submit\" value=\"Edit\">  <input type=hidden name="f" value="0"></form></body></head></html>"""
                return doc
         elif docc=='Fee Structure Certificate For Bank':
                doc+="""<html>Click On Button To Edit!!!<head><body><form value="form" action="read_bank.py" method="post"><input type=\"submit\" value=\"Edit\">  <input type=hidden name="f" value="2"></form></body></head></html>"""
                return doc
        
def print_Application_stud(req):
           
           session = Session.Session(req);
           Rollno=session['rno']
           session.save()
           session.cleanup()
           tabid="ApplicationRequests"
           db = MySQLdb.connect(
    	   host="localhost",
    	   user=data.mysql_user,
    	   passwd=data.mysql_pswd,
    	
           db="userInputDatabase" )
   	   #prepare a cursor object using cursor() method
    	   cursor = db.cursor()
           info=req.form
           ff=int(info['f'])
           
           arrayid=["APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate","APND,ApplicationFormFilled,ApplicationSubmitted,No Dues Certificate,apply for No Dues Certificate"
,"APFS,ApplicationFormFilled,ApplicationSubmitted,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","APIB,ApplicationFormFilled,ApplicationSubmitted,International Bonafide Certificate,apply for International Bonafide Certificate","APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate"]
          
           psid=arrayid[ff]
           appid=psid.split(',')[0]
           aplydc=psid.split(',');
           aplydc=aplydc[3:]
          	
           ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
           cursor.execute(ss,(Rollno,appid+'%'))
           val=cursor.fetchall()
           states=val[len(val)-1]
         

           if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled'):
           	 flg=1
	  	 ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values (NOW(),"insert",%s,%s,%s);"""

                 cursor.execute(ss,(Rollno,tabid,appid+",ApplicationFormFilled,ApplicationFormFilled,"+aplydc[0]))
         	 db.commit();




           ss="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values (NOW(),"insert",%s,%s,%s);"""
           cursor.execute(ss,(Rollno,tabid,psid))
       	   db.commit();
           
           
          fp=open(data.path+"/project_data/autoclick4.html")
          fp=fp.read()   
          return fp
