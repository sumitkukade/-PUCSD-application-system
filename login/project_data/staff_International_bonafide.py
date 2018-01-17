from config_path import data
import MySQLdb
import time;
import refno
from mod_python import Session
from config_path import data
import student
def submit_success(req):
         flag=0
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
         cursor.execute(ss2,(Rollno,'APIB'))
         valq=cursor.fetchall()
               
         statess=valq[len(valq)-1]
         
         
         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
                flag=1;
        
         	ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
        	cursor.execute(ss,(sname,ip,"APIB,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",International Bonafide Certificate,apply for International Bonafide"))
         	db.commit()       
         
         
         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1  or statess[1]=='ApplicationModification':

         	dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	cursor.execute(dd,(sname,ip,"APIB,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",International Bonafide Certificate,apply for International Bonafide"))
         	db.commit()
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp
def index(req):
         Rollno=refno.Rollno
         
         info=req.form
         rfno=info['dossss']
         rpno=info['repno']
         unino=info['uno'];
         svup=info['uto'];
         rob=info['rob'];
         dt=info['date'];
         Rollno=info['rln'];
	 Ed=info['ed']
	 Rd=info['rd']
         global ff
         ff=3
         flg=0
         doc='';
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase" )
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         




	 chkref="""select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s;"""%(Rollno)
         cursor.execute(chkref)
         valref=cursor.fetchall()
         valref= map(lambda x:int(x[0]),valref)
	 
	 if int(refn) in valref:
		 ss="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId ='ERR';"""
         	 cursor.execute(ss)
                 em=cursor.fetchall()[0][0]
		
		 return """</form><html><link rel="stylesheet" href="./code.css"/><form value="form" action="./refno.py" method="post"><ul><li><a  class="active"  href="./log_staff.py">HOME</a></li><li style="float:right"><a href="./logout.py">LOGOUT</a></li></ul><br><font size=3><b>%s</b></font><br><br><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value='%s'><input type=\"submit\"value=\"OK\"></form></html>"""%(em, Rollno,"International Bonafide Certificate")     





	

                
         ss="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
         cursor.execute(ss,(Rollno,'APIB'+'%'))
         val=cursor.fetchall()
         
         
         states=val[len(val)-1]
         chkref="""select %s in (select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s);"""
         cursor.execute(chkref,(refno,Rollno))
         valref=cursor.fetchall()
         valref= map(lambda x:x[0],valref)
         
         if valref[0]==1:
              chkref1="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId="Err";"""
              cursor.execute(chkref1)
              valref1=cursor.fetchall()
              return """</form><html><b>%s</b><form value="form" action="./refno.py" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(valref1[0])
         
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess" )
         # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
             
          
         fp=open(data.path+"/project_data/staff_INTBN.html","r")
         fp=(fp.read());


           
	 ss = """select * from applicationProcess.studentDetailsDomain where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()

         ss1 = """select * from applicationProcess.internationalStudentInformationDomain where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss1)
       	 val1=cursor.fetchall()


         ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APIB';"""%(Rollno)
         cursor.execute(ss)
         valu=cursor.fetchall(); 
         db.commit()
         
         if(len(valu)==0):
             ss= """insert into applicationProcess.applicationFormForStaff values(NULL,%s,'APIB','',%s,%s,%s,%s,%s,%s,%s) ;"""
             cursor.execute(ss,(Rollno,int(rfno),int(rpno),int(unino),int(svup),rob,Ed,Rd)) 
             db.commit()
        
         else:
		ss="""update applicationProcess.applicationFormForStaff set refNo=%s,rpNo=%s,UniqueNo=%s,stayVisaUpTo=%s,regularOrBacklog=%s,examDate=%s,resultDate=%s where rollNumber=%s and appId='APIB'"""
                cursor.execute(ss,(int(rfno),int(rpno),int(unino),int(svup),rob,Ed,Rd,Rollno))
                db.commit()     	

         
              
	 sss4="""select * from applicationProcess.officeContactDetails;"""
    	 cursor.execute(sss4)
       	 vall4=cursor.fetchall()
         email_phone = map(lambda x:x,vall4)  
     
         doc+="""<h1>International Bonafide Certificate:<br><br><br> <h1>"""       
	 
         d=time.strftime("%d/%m/%Y")

         doc+=fp%(email_phone[0][0],email_phone[0][1],rfno,dt,val[0][4]+" "+val[0][5]+" "+val[0][6],val[0][4]+" "+val[0][5]+" "+val[0][6],val1[0][1],val1[0][2].title(),int(val[0][9]), rpno,unino,int(val1[0][4]),int(val1[0][7]),val1[0][5],val1[0][8],val1[0][6],val1[0][9],val1[0][10],svup,val1[0][3],val[0][1],val[0][1],d,rob.title(),Ed,Rd,str(d));

         doc+="""<html><head><body><div class="inner"><form value="form" action="staff_International_bonafide.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=\"submit\" value=\"Submit\"></form></div>&nbsp&nbsp<div class="inner"><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value=\"APIB\"><input type=\"submit\"  value=\"Edit\"></form></div>&nbsp&nbsp<div class="inner"><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APIB\"><input type=\"submit\" value=\"REJECT\"></form></div></body></head></html>"""%(Rollno,Rollno,Rollno)

        

         return doc
