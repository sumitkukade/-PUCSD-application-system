from config_path import data
import MySQLdb
import time;
from mod_python import Session
from config_path import data
import student
def submit_success(req):

         flag=0;
         info=req.form
         session = Session.Session(req);
         
         try:
           sname=session['sno'];
         except:
           return """<html>Session Expired<p><a href="../../staff_log.html"> LOGIN AGAIN</a></html>"""
	 prp=info['pops']
         edit=info['fpr']
	 refn=info['refn']
         ip=session['ipaddr']
         session.save()
         session.cleanup()
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")
	 p=prp
         cursor = db.cursor()
         Rollno=info['rol']
         a=int(refn)
	
	
	 ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
         cursor.execute(ss,(Rollno,edit))
         valu=cursor.fetchall(); 
         db.commit()

         
         if(len(valu)==0):
	     
             ss= """select * from applicationProcess.applicationFormForStaff where  rollNumber=%s and applicationPurpose=%s and appid="APBN";"""
             cursor.execute(ss,(Rollno,p)) 
             hre=cursor.fetchall();
	     hre=map(lambda x:x,hre)
             	
             if (len(hre)==0):
                	 ss= """insert into applicationProcess.applicationFormForStaff values(NULL,%s,'APBN',%s,%s,0,0,0,'',NULL,NULL) ;"""
            		 cursor.execute(ss,(Rollno,p,a)) 
             		 db.commit()
                	     
	     		 ss="""update applicationProcess.aux_studentAndState set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	     		 cursor.execute(ss,(p,Rollno,edit))
	    		 db.commit()

 			 ss="""update applicationProcess.applicationForm set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	     		 cursor.execute(ss,(p,Rollno,edit))
	    		 db.commit()
			 ss="""update applicationProcess.studentApplicationQueue set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	     	         cursor.execute(ss,(p,Rollno,edit))
	    	         db.commit()	        
	 
			 
			 ss="""update applicationProcess.requestStateTransitions set applicationPurpose=%s where userId=%s and applicationPurpose=%s;"""
	     		 cursor.execute(ss,(p,Rollno,edit))
	    		 db.commit()
			 ss="""update  userInputDatabase.staffTable set Document="Bonafide Certificate For "%s where RollNo=%s and Document="Bonafide Certificate For "%s;"""
	     		 cursor.execute(ss,(p,Rollno,edit))
	    		 db.commit()

         else:
		ss="""update applicationProcess.aux_studentAndState set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	        cursor.execute(ss,(p,Rollno,edit))
	    	db.commit()
		ss="""update applicationProcess.applicationFormForStaff set applicationPurpose=%s,refNo=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s"""
                cursor.execute(ss,(p,a,Rollno,edit))
                db.commit()
		ss="""update applicationProcess.aux_studentAndState set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
		cursor.execute(ss,(p,Rollno,edit))
		db.commit()
		ss="""update applicationProcess.requestStateTransitions set applicationPurpose=%s where userId=%s and applicationPurpose=%s;"""
	        cursor.execute(ss,(p,Rollno,edit))
	        db.commit()
		ss="""update  userInputDatabase.staffTable set Document="Bonafide Certificate For "%s where RollNo=%s and Document="Bonafide Certificate For "%s;"""
	     	cursor.execute(ss,(p,Rollno,edit))
	        db.commit()
		ss="""update applicationProcess.studentApplicationQueue set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	     	cursor.execute(ss,(p,Rollno,edit))
	    	db.commit()	        


 	        ss="""update applicationProcess.applicationForm set applicationPurpose=%s where rollNumber=%s and appId='APBN' and applicationPurpose=%s;"""
	     	cursor.execute(ss,(p,Rollno,edit))
	    	db.commit()















         
         ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s and applicationPurpose=%s;"""
         cursor.execute(ss2,(Rollno,'APBN',prp))
         valq=cursor.fetchall()
               
         statess=valq[len(valq)-1]
         
    
         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
                 flag=1;
                 
                 
        	 ss2="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	 cursor.execute(ss2,(sname,ip,"APBN,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",Bonafide Certificate,"+prp))
         	 db.commit()       
         	          
         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1 or statess[1]=='ApplicationModification':

        	 dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	 cursor.execute(dd,(sname,ip,"APBN,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",Bonafide Certificate,"+prp))
         	 db.commit()
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp
def index(req):
         info=req.form;
         refn=info['dossss']
         dat=info['date']
         purp1=info['purp']
         Rollno=info['rln']
         fp=open(data.path+"/project_data/staff_bonafied.html");
         edit=info['prps']
         fp=fp.read();
         session = Session.Session(req);
         doc='';
	 	 
         if len(purp1)!=0:
		p=purp1;
         else:
		p=edit
         

         doc='' 
	 db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")

         cursor = db.cursor()
         
         

	 
	 chkref="""select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s;"""%(Rollno)
         cursor.execute(chkref)
         valref=cursor.fetchall()
         valref= map(lambda x:int(x[0]),valref)
	 
	 if int(refn) in valref:
		 ss="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId ='ERR';"""
         	 cursor.execute(ss)
                 em=cursor.fetchall()[0][0]
		
		 return """</form><html><link rel="stylesheet" href="./code.css"/><form value="form" action="./refno.py" method="post"><ul><li><a  class="active"  href="./log_staff.py">HOME</a></li><li style="float:right"><a href="./logout.py">LOGOUT</a></li></ul><br><font size=3><b>%s</b></font><br><br><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value='%s'><input type=\"submit\"value=\"OK\"></form></html>"""%(em, Rollno,"Bonafide Certificate For "+edit)     
         

         
	 ss="""select applicationPurpose from applicationProcess.aux_studentAndState where  rollNumber=%s and appid="APBN" and applicationPurpose!=%s;"""
         cursor.execute(ss,(Rollno,edit))
         arvl=cursor.fetchall()
         
	 arvl=map(lambda x:x[0],arvl);
         if purp1 in arvl:
		 ss="""select  msgForState  from userInputDatabase.messagesForUsersDomain where msgId ='Start';"""
         	 cursor.execute(ss)
                 em=cursor.fetchall()[0][0]
		 return """</form><html><link rel="stylesheet" href="./code.css"/><form value="form" action="./refno.py" method="post"><ul><li><a  class="active"  href="./log_staff.py">HOME</a></li><li style="float:right"><a href="./logout.py">LOGOUT</a></li></ul><br><font size=3><b>%s</b></font><br><br><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value='%s'><input type=\"submit\"value=\"OK\"></form></html>"""%(em, Rollno,"Bonafide Certificate For "+edit)     
         
	 ss="""select * from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss)
       	 val=cursor.fetchall()
         add1=val[0][12].title()
         add2=val[0][13].title()
         add3=val[0][14].title()
         
         y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         cursor.execute(y,(Rollno,Rollno))
         val1=cursor.fetchall()
         yy= map(lambda x:x[0],val1)
         d=time.strftime("%d/%m/%Y")
         year=int(d.split('/')[2])
         per=edit
        
         a=int(refn)
         
         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
             hh="his"
         else:
             gen='Miss.'
             hh="her"


	

	 ss4="""select courseId  from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss4)
       	 val4=cursor.fetchall()
         cnm = map(lambda x:x[0],val4)         
         if (cnm[0]=='mca'):
             cname='Master of Computer Applications(Science)' 
             
         else:
             cname='Master of Science(Computer Science)'
	


         
         dt="""select  dateOfBirth from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
         cursor.execute(dt)
         valdt=cursor.fetchall()    
         bdt= map(lambda x:x[0],valdt)
         dt=str(bdt[0]).split('-')
         dt.reverse()
         dt='-'.join(dt)
         sss4="""select * from applicationProcess.officeContactDetails;"""
    	 cursor.execute(sss4)
       	 vall4=cursor.fetchall()
         email_phone = map(lambda x:x,vall4)  
         doc+=fp%(email_phone[0][0],email_phone[0][1],refn,dat,gen,val[0][4]+" "+val[0][5]+" "+val[0][6],int(val[0][0]),cname,yy[0],year,year+1,hh,p,add1,add2,add3,dt);

        

	 
         
         doc+="""<div class="inner"><html><head><body><form value="form" action="staff_bonafied.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=hidden name=\'refn\' value='%s'><input type=hidden name=\'pops\' value=\'%s\'><input type=hidden name=\'fpr\' value=\'%s\'><input type=\"submit\" value=\"Submit\"></form></div>&nbsp&nbsp<div class="inner"><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value='%s'><input type=\"submit\"  value=\"Edit\"></form></div>&nbsp&nbsp<div class="inner"><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APBN\"><input type=hidden name=\'prps\' value=\'%s\'><input type=\"submit\" value=\"REJECT\"></form></div></body></head></html>"""%(Rollno,refn,p,edit,Rollno,"Bonafide Certificate For "+edit,Rollno,edit)   
         return doc






