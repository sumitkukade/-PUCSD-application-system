import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session
Rollno=0;
def index(req):
    global Rollno 
    info=req.form;
    Rollno=info['rono'];
    doc=info['docm']
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase")
     
    cursor = db.cursor()
    if ('Bonafide Certificate' in doc) and ('International Bonafide Certificate' not in doc) or doc=='APBN':
      fp1=open(data.path+"/project_data/staff_ref_date.html");
      fp1=fp1.read();
      db = MySQLdb.connect(
      host="localhost",
      user=data.mysql_user,
      passwd=data.mysql_pswd,
      db="userInputDatabase")
      # prepare a cursor object using cursor() method
      cursor = db.cursor();
      session = Session.Session(req);
      try:
	if session['prps']!='':
      		doc=session['prps'];
                doc='Bonafide Certificate For '+doc
		session.save()
	else:
		doc=doc
      except:
	    doc=doc
      session['prps']=''
      edit=doc
      edit=edit.split('Bonafide Certificate For')
	
      edit=edit[1].strip()

     
      p="""select refNo from applicationProcess.applicationFormForStaff where appId='APBN' and rollnumber=%s and applicationPurpose=%s;"""
      cursor.execute(p,(Rollno,edit))
      referense_no=cursor.fetchall();
      
      referense_no= map(lambda x:x[0],referense_no)
      
      if len(referense_no)!=0:
           referense_no=referense_no[0]
      else:
           referense_no='';
      	
      p="""select applicationPurpose from applicationProcess.applicationForm where appId='APBN' and rollnumber=%s;"""%(Rollno)
      cursor.execute(p)
      val2=cursor.fetchall()
      add2= map(lambda x:x[0],val2)[0]
      
      


      
      fp11=fp1%((referense_no),Rollno,edit,edit,edit,edit)
      return """<html>%s</html>"""%(fp11)
    elif doc=='Fee Structure Certificate For Bank' or doc=='APFS':


         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="userInputDatabase")
   	 # prepare a cursor object using cursor() method
    	 cursor = db.cursor()
         p="""select applicationPurpose from applicationProcess.applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         val2=cursor.fetchall()
         add1= map(lambda x:x[0],val2)
         
         fp1=open(data.path+"/project_data/staff_bank_addr.html");
         fp1=fp1.read();


         p="""select refNo from applicationProcess.applicationFormForStaff where appId='APFS' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)
         referense_no=cursor.fetchall();
         referense_no= map(lambda x:x[0],referense_no)  
         if len(referense_no)!=0:
           referense_no=referense_no[0]
         else:
           referense_no='';
  	 
         	
         return fp1%(referense_no,Rollno,str(add1[0]))
    elif doc=='No Dues Certificate' or doc=='APND':
         fp1=open(data.path+"/project_data/staff_no_dues.html");
         p="""select refNo from applicationProcess.applicationFormForStaff where appId='APND' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)

         referense_no=cursor.fetchall();
         referense_no= map(lambda x:x[0],referense_no)  
         if len(referense_no)!=0:
           referense_no=referense_no[0]
         else:
           referense_no='';

         fp1=fp1.read()%(referense_no,Rollno);
             
         return """<html>%s</html>"""%(fp1)
    elif doc=='International Bonafide Certificate' or doc=='APIB':
         fp1=open(data.path+"/project_data/staff_International_bonafide.html");
         fp1=fp1.read();
         p="""select refNo from applicationProcess.applicationFormForStaff where appId='APIB' and rollnumber=%s;"""%(Rollno)
         cursor.execute(p)

         referense_no=cursor.fetchall();
         referense_no= map(lambda x:x[0],referense_no)  
         if len(referense_no)!=0:
           referense_no=referense_no[0]
         else:
           referense_no='';

         return fp1%(referense_no,Rollno);
