import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session

def submit_success(req):

         flag=0;   
         info=req.form
         session = Session.Session(req);
         
         try:
            sname=session['sno'];
         except:
           return """<html>Session Expired<p><a href="../../staff_log.html"> LOGIN AGAIN</a></html>"""

         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")

         cursor = db.cursor()
         Rollno=info['rol']
         
         ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s;"""
         cursor.execute(ss2,(Rollno,'APND'))
         valq=cursor.fetchall()
              
         statess=valq[len(valq)-1]
         

         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
                 flag=1;
         	 ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
                 cursor.execute(ss,(sname,ip,"APND,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",No Dues Certificate,apply for No Dues Certificate"))
         	 db.commit()       
         
         

         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1 or statess[1]=='ApplicationModification':

         	dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	cursor.execute(dd,(sname,ip,"APND,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",No Dues Certificate,apply for No Dues Certificate"))
         	db.commit()
        
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp







def index(req):
         
         info=req.form
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")
         refn=info['dossss']
         d=info['dd']
         cursor = db.cursor()
         Rollno=info['rln']   
         doc=''
         
         fp=open(data.path+"/project_data/staff_no_dues_docoment.html","r")
         fp=(fp.read());



	 chkref="""select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s;"""%(Rollno)
         cursor.execute(chkref)
         valref=cursor.fetchall()
         valref= map(lambda x:int(x[0]),valref)
	 
	 if int(refn) in valref:
		 ss="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId ='ERR';"""
         	 cursor.execute(ss)
                 em=cursor.fetchall()[0][0]
		
		 return """</form><html><link rel="stylesheet" href="./code.css"/><form value="form" action="./refno.py" method="post"><ul><li><a  class="active"  href="./log_staff.py">HOME</a></li><li style="float:right"><a href="./logout.py">LOGOUT</a></li></ul><br><font size=3><b>%s</b></font><br><br><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value='%s'><input type=\"submit\"value=\"OK\"></form></html>"""%(em, Rollno,"No Dues Certificate")     


         ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APND';"""%(Rollno)
         cursor.execute(ss)
         valu=cursor.fetchall(); 
         db.commit()


         a=refn;
         if(len(valu)==0):
             ss= """insert into applicationProcess.applicationFormForStaff values(NULL,%s,'APND','',%s,0,0,0,'',NULL,NULL) ;"""
             cursor.execute(ss,(Rollno,a)) 
             db.commit()
         else:
		ss="""update applicationProcess.applicationFormForStaff set refNo=%s where rollNumber=%s and appId='APND'"""
                cursor.execute(ss,(a,Rollno))
                db.commit()     	



         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
             on_print_gender="him"
         else:
             gen='Miss.'
             hh="her"
	     on_print_gender="her"

         ss4="""select courseId  from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss4)
       	 val4=cursor.fetchall()
         cnm = map(lambda x:x[0],val4)         
         if (cnm[0]=='mca'):
             cname='Master of Computer Applications(Science)' 
             
         else:
             cname='Master of Science(Computer Science)'
         chkref="""select %s in (select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s);"""
         cursor.execute(chkref,(refn,Rollno))
         valref=cursor.fetchall()
         valref= map(lambda x:x[0],valref)
         
         if valref[0]==1:
              chkref1="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId="Err";"""
              cursor.execute(chkref1)
              valref1=cursor.fetchall()
              return """</form><html><b>%s</b><form value="form" action="./refno.py" method="post"><input type=\"submit\"value=\"OK\"><input type=hidden name='rono' value='%s'><input type=hidden name='docm' value='%s'></form></html>"""%(valref1[0][0],Rollno,'APND')
    
         ss="""select * from  studentDetailsDomain where rollNumber=%s;;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         sss4="""select * from applicationProcess.officeContactDetails;"""
    	 cursor.execute(sss4)
       	 vall4=cursor.fetchall()
         email_phone = map(lambda x:x,vall4) 
         doc+=fp%(email_phone[0][0],email_phone[0][2],refn,d,gen,val[0][4]+" "+val[0][5]+" "+val[0][6]+" ",int(val[0][0]),cname,on_print_gender,hh);
         doc+="""<html><head><body><div class="inner"><form value="form" action="staff_no_dues.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=\"submit\" value=\"Submit\"></form></div>&nbsp&nbsp<div class="inner"><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value=\"APND\"><input type=\"submit\"  value=\"Edit\"></form></div>&nbsp&nbsp<div class="inner"><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APND\"><input type=\"submit\" value=\"REJECT\"></form></div></body></head></html>"""%(Rollno,Rollno,Rollno)
         return doc
