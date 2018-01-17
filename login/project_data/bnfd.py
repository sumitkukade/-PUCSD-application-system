import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session
def addr_split(nn):
               cnt=0
               cntt=0
          
               nn=list(nn)
               for i in range(0,len(nn)):
                   if nn[i]==',':
                        nn[i]='</br>';
                        cntt=1
                   elif nn[i]==' ':
                       cntt+=1;
                       if cntt%3==0:
                           nn[i]='</br>';


               return nn;
def submit_success(req):

         flag=0;   
         info=req.form
         session = Session.Session(req);
         session.load()
         try:
           sname=session['sno'];
         except:
            return """<html>Session Expired<p><a href="../../staff_log.html"> LOGIN AGAIN</a></html>"""

         ip=session['ipaddr']
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")

         cursor = db.cursor()
         Rollno=info['rol']
         ss2="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId= %s;"""
         cursor.execute(ss2,(Rollno,'APFS'))
         valq=cursor.fetchall()
               
         statess=valq[len(valq)-1]
         

         
         
         if statess==('ApplicationSubmitted', 'RequestArrivedInOffice') and flag==0:
   	              flag=1;
         

   		      ss="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
   		      cursor.execute(ss,(sname,ip,"APFS,RequestArrivedInOffice,ApplicationModification,"+str(Rollno)+",Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank"))
   		      db.commit()       
         
         
         if statess==('RequestArrivedInOffice', 'ApplicationModification') or flag==1 or statess[1]=='ApplicationModification':

         
         	dd="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
         	cursor.execute(dd,(sname,ip,"APFS,ApplicationModification,ModificationSuccessfully,"+str(Rollno)+",Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank"))
         	db.commit()
        	
         fp=open(data.path+"/project_data/autoclick3.html")
         fp=fp.read()   
         return fp
def index(req):

         info=req.form
         refn=info['dossss']
         dat=info['date']
         badr=info['bank'];
         Rollno=info['rln']
         
         a=refn
         doc='';
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         p="""select applicationPurpose from applicationProcess.applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         val2=cursor.fetchall()
         add= map(lambda x:x[0],val2)
          
         chkref="""select refNo from applicationProcess.applicationFormForStaff where rollNumber!=%s;"""%(Rollno)
         cursor.execute(chkref)
         valref=cursor.fetchall()
         valref= map(lambda x:int(x[0]),valref)
	 
	 if int(refn) in valref:
		 ss="""select msgForAcomplish from userInputDatabase.messagesForUsersDomain where msgId ='ERR';"""
         	 cursor.execute(ss)
                 em=cursor.fetchall()[0][0]
		
		 return """</form><html><link rel="stylesheet" href="./code.css"/><form value="form" action="./refno.py" method="post"><ul><li><a  class="active"  href="./log_staff.py">HOME</a></li><li style="float:right"><a href="./logout.py">LOGOUT</a></li></ul><br><font size=3><b>%s</b></font><br><br><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value='%s'><input type=\"submit\"value=\"OK\"></form></html>"""%(em, Rollno,"Fee Structure Certificate For Bank")  
              
       
         fp=open(data.path+"/project_data/staff_fee_structure.html","r")
         fp1=open(data.path+"/project_data/staff_fee_structure2.html","r")
         fp1=fp1.read()
         fp=(fp.read());
         
         p="""select applicationPurpose from applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         val2=cursor.fetchall()
         purpose= map(lambda x:x[0],val2)
         if(len(badr)!=0):
            ss= """update applicationProcess.applicationForm set applicationPurpose=%s where appId="APFS" and rollnumber=%s;"""
            cursor.execute(ss,(badr,Rollno)) 
            db.commit()
            p=badr
         else:
             p=purpose[0]

         	
         ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId='APFS';"""%(Rollno)
         cursor.execute(ss)
         valu=cursor.fetchall(); 
         db.commit()



         if(len(valu)==0):
             ss= """insert into applicationProcess.applicationFormForStaff values(NULL,%s,'APFS',%s,%s,0,0,0,'',NULL,NULL) ;"""
             cursor.execute(ss,(Rollno,p,a)) 
             db.commit()
         else:
		ss="""update applicationProcess.applicationFormForStaff set applicationPurpose=%s,refNo=%s where rollNumber=%s and appId='APFS'"""
                cursor.execute(ss,(p,a,Rollno))
                db.commit()     	
	 
	 
	 addr=p.split(',');
	 addr1=','.join(addr[1:]);
        
         addr2=''.join(addr_split(addr1))
         
         p=addr[0]+"<br>"+addr2
         
	 

	 p=p.title()
         ss="""select * from applicationProcess.feesStructureForm where rollNumber=%s ;"""%(Rollno)
    	 cursor.execute(ss)
       	 val6=cursor.fetchall()
         val=val6
         ss3="""select gender from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss3)
       	 val3=cursor.fetchall()
         g = map(lambda x:x[0],val3)         
         if (g[0]=='m'):
             gen='Mr.'
         else:
             gen='Miss.'
  	 ss4="""select courseId  from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss4)
       	 val4=cursor.fetchall()
         cnm = map(lambda x:x[0],val4)         
         if (cnm[0]=='mca'):
             cname='Master of Computer Applications(Science)' 
             
         else:
             cname='Master of Science(Computer Science)'
         
	 ss5="""select category from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 cursor.execute(ss5)
       	 val5=cursor.fetchall()
         catgry = map(lambda x:x[0],val5) 
         sss4="""select * from applicationProcess.officeContactDetails;"""
    	 cursor.execute(sss4)
       	 vall4=cursor.fetchall()
         email_phone = map(lambda x:x,vall4) 
         yy="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         cursor.execute(yy,(Rollno,Rollno))
         val111=cursor.fetchall()
         yy= map(lambda x:x[0],val111)
         if (yy[0]=='1'):
             yyy='1 st'
         elif(yy[0]=='2'):
             yyy='2 nd'
         else:
             yyy='3 rd'    
    	 if val[0][4]=='mca':  
           doc+=fp1%(email_phone[0][0],email_phone[0][2],refn,dat,p,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],yyy,cname,catgry[0],val[0][6],val[1][6],val[2][6],val[3][6],val[4][6],val[5][6],val[0][7],val[1][7],val[2][7],val[3][7],val[4][7],val[5][7],val[0][8],val[1][8],val[2][8],val[3][8],val[4][8],val[5][8],val[0][9],val[1][9],val[2][9],val[3][9],val[4][9],val[5][9])
         else:
		doc+=fp%(email_phone[0][0],email_phone[0][2],refn,dat,p,gen,val[0][1]+" "+val[0][2]+" "+val[0][3],yyy,cname,catgry[0],val[0][6],val[1][6],val[2][6],val[3][6],val[0][7],val[1][7],val[2][7],val[3][7],val[0][8],val[1][8],val[2][8],val[3][8],val[0][9],val[1][9],val[2][9],val[3][9])


     
         doc+="""<html><head><body><div class="inner"><form value="form" action="bnfd.py/submit_success" method="post"><input type=\"hidden\" name=\"rol\" value=%s><input type=\"submit\" value=\"Submit\"></form></div>&nbsp&nbsp<div class="inner"><form value="form" action=\"refno.py\"><input type=\"hidden\" name=\"rono\" value=%s><input type=\"hidden\" name=\"docm\" value=\"APFS\"><input type=\"submit\"  value=\"Edit\"></form></div>&nbsp&nbsp<div class="inner"><form value=\"form\" action=\"reject.py\" method=\"post\"><input type=hidden name=\"rono\" value=%s><input type=hidden name=\"docm\" value=\"APFS\"><input type=\"submit\" value=\"REJECT\"></form></div></body></head></html>"""%(Rollno,Rollno,Rollno)


  	 return doc

