import MySQLdb
import re  
from mod_python import Session
from config_path import data

def split_uppercase(s):
            return re.sub(r'([^A-Z])([A-Z])', r'\1 \2',s)


def index(req):
    web_page=""

      
    session = Session.Session(req)
    try:
      rollno=session['rno']
    except:
        	return """<html>Session Expired<p><a href="../student-login.html"> LOGIN AGAIN</a></html>"""
  


    ip=session['ipaddr']
    session.save()
    session.cleanup()
    req.content_type = 'text/html'
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="applicationProcess" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    query="""DROP TABLE IF EXISTS userInputDatabase.StudentStatus;""";
    cursor.execute(query);
    db.commit()

    queryw="""select appId from applicationProcess.applicationDomain;"""
    cursor.execute(queryw)
    ress=cursor.fetchall()
    ress=map(lambda x:x[0],ress);
    
    arry=[] 	
    
    for i in ress:
	if i=='APBN':
		query="""select applicationPurpose from applicationProcess.applicationForm where rollNumber=%s and appid='APBN';"""
       	        cursor.execute(query,(rollno,));
       	        query_result=cursor.fetchall()
       	        query_result=map(lambda x:x[0],query_result)	
		
		for i in list(set(query_result)):
    			queryw="""select toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId='APBN' and applicationPurpose=%s order by requestId desc limit 1 ;"""
    			cursor.execute(queryw,(rollno,i))
    			ress1=cursor.fetchall()
    			ress1=map(lambda x:x[0],ress1)
     			
    			if len(ress1)!=0 and ress1[0]=='FormPrinted':
        	    		arry.append(i)
	else:
		queryw="""select toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId='%s' order by requestId desc limit 1 ;"""%(rollno,i)
    		cursor.execute(queryw)
    		ress1=cursor.fetchall()
    		ress1=map(lambda x:x[0],ress1)
     
    		if len(ress1)!=0 and ress1[0]=='FormPrinted':
        	    arry.append(i)
    	       
    file=open(data.path+"/project_data/nevtag1.html","r");
    file=file.read()
    req.write(file)
    
    if len(arry)!=0:
        docc=''
	
        for i in range(0,len(arry)):
        	qqq="""select appDesc from  applicationProcess.applicationDomain where appId='%s';"""%(str(arry[i])) 	
		cursor.execute(qqq)
        	ans=cursor.fetchall()
	
		
		if len(ans)==0:
		   ans="Bonafide Certificate For %s"%(arry[i])
		else:
		    ans=map(lambda x:x[0],ans)[0]
		if len(arry)-1!=i:
        		docc+=ans+","
		else:
			docc+=ans;
        
        aa="""</br><html><MARQUEE><blink><font size=4><b>Your  <i><font color=\"red\">%s </font></i>Is Printed Please Visite Office Along With Your Id Card!!!</b></font></blink></MARQUEE></html>"""%(docc)
        req.write(aa)   
    
    q="""select fname,mname,lname from applicationProcess.studentDetailsDomain where rollNumber=%s;"""%(rollno)
    cursor.execute(q);
    name_of_student=cursor.fetchall()
   
    if len(name_of_student)==0:
       return """access denied!!"""	
    name_of_student=name_of_student[0]
    name_of_student=' '.join(name_of_student);
    name_of_student=name_of_student.title()
    req.write("<label>Name:</b></label><label>"+name_of_student+"</label>")


    req.write('<b><p><label>Rollno: %s\n</b></label>' % session['rno'])

    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method

   
    query="""DROP TABLE IF EXISTS userInputDatabase.StudentStatus;""";
    cursor.execute(query);
    db.commit()
    table="""create table userInputDatabase.StudentStatus (RollNumber%s int,Documents%s text,Status%s text);"""%(rollno,rollno,rollno);
    cursor.execute(table);
    db.commit()
    query="""select appDesc from applicationProcess.applicationDomain """
    cursor.execute(query);
    query_result=cursor.fetchall()
    appname=map(lambda x:x[0],query_result)
    
    
    query="""select appId from applicationProcess.applicationDomain """
    cursor.execute(query);
    query_result=cursor.fetchall()
    appid=map(lambda x:x[0],query_result)
        
    
    appl=['Bonafide Certificate','Fee Structure Certificate For Bank','International Bonafide Certificate','No Dues Certificate']
     
    
    for i in range(0,len(appid)):
      if appid[i]=='APBN':
       	query="""select applicationPurpose from applicationProcess.applicationForm where rollNumber=%s and appid='APBN';"""
       	cursor.execute(query,(rollno,));
       	query_result=cursor.fetchall()
       	query_result=map(lambda x:x[0],query_result)
    	    
        
        for j in list(set(query_result)):

                    query="""select params,applicationPurpose from applicationProcess.requestStateTransitions where userId=%s and applicationPurpose=%s and params like %s"""
                    cursor.execute(query,(rollno,j,appid[i]+'%'));
                    query_result=cursor.fetchall()
                    
                    if len(query_result)!=0:  
                        stsfm=str(query_result[len(query_result)-1]).split(',')[1]
                        ststo=str(query_result[len(query_result)-1]).split(',')[2]
                        query_result=map(lambda x:x,query_result)
                        dblcm=str(query_result[len(query_result)-1]).split(',')[4]
	                dblcm=map(lambda x:x, query_result[len(query_result)-1])[1]
	
                
                        if ststo=='ApplicationSubmitted':

                                            query="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s and applicationPurpose=%s  order by requestId desc limit 1 ;"""
                                            cursor.execute(query,(rollno,appid[i],j));   
                                            ree=cursor.fetchall()
                                            ree=map(lambda x:x,ree)
                                            b=split_uppercase(ree[0][1])
                              
                                            if len(ree)!=0:
                   
                                                        query="""insert into StudentStatus values(%s,%s,%s)"""
                                                        cursor.execute(query,(rollno,appname[i]+" For "+dblcm,b))
                                                        db.commit();
                                
                        else:
                                                b=split_uppercase(ststo)
                                                query="""insert into StudentStatus values(%s,%s,%s)"""
                                                cursor.execute(query,(rollno,appname[i]+" For "+dblcm,b));
                                                db.commit();
	
        
      else:
       
       query="""select params,applicationPurpose from applicationProcess.requestStateTransitions where userId=%s and params like %s"""
       cursor.execute(query,(rollno,appid[i]+'%'));
       query_result=cursor.fetchall()

       if len(query_result)!=0:  
                stsfm=str(query_result[len(query_result)-1]).split(',')[1]
                ststo=str(query_result[len(query_result)-1]).split(',')[2]
                query_result=map(lambda x:x,query_result)
                dblcm=str(query_result[len(query_result)-1]).split(',')[4]
	        dblcm=map(lambda x:x, query_result[len(query_result)-1])[1]
	         
                
                if ststo=='ApplicationSubmitted':
                             	
                         
                              query="""select fromState,toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s   order by requestId desc limit 1 ;"""
                              cursor.execute(query,(rollno,appid[i]));   
                              ree=cursor.fetchall()
                              ree=map(lambda x:x,ree)
                              b=split_uppercase(ree[0][1])
                              b=b.strip()
                                
                              if len(ree)!=0:
                                      
                                      query="""insert into StudentStatus values(%s,%s,%s)"""
                                      cursor.execute(query,(rollno,appname[i],b))
                                      db.commit();
                                      
                                
                else:
                      b=split_uppercase(ststo)
                      query="""insert into StudentStatus values(%s,%s,%s)"""
                      cursor.execute(query,(rollno,appname[i],b));
                      db.commit();
    
   
    
  
    
  
            
    









	
       
    cursor.execute(""" select * from StudentStatus;""");
    query_result=cursor.fetchall()
    names = list(map(lambda x: x[0], cursor.description))
    db.close() 
    fp1=open(data.path+"/project_data/json.txt","w");
    fp1.write("[");
    for i in range(0,len(query_result)):
        fp1.write("{");
    	for n in range(0,len(names)):
		fp1.write("\""+str(names[n])+"\":");
		if str(query_result[i][n]).isdigit():
                	fp1.write(str(query_result[i][n]));
		else:
	                fp1.write("\""+str(query_result[i][n])+"\"");
		
		if not n==len(names)-1:
		  fp1.write(",\n");
	if not i==len(query_result)-1:
        	fp1.write("},\n");
	else:
		fp1.write("}	\n");
		

    fp1.write("]");
   
    
    #crp=open(data.path+"/project_data/sample.html","r");
    #web_page+=crp.read()
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    query="""select output from outputResults;"""
    cursor.execute(query)
    apsts=cursor.fetchall()
    req.content_type="text/html"
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    db.close()
    
   

    query=""" select rollNumber from applicationProcess.internationalStudentInformationDomain;"""
    cursor.execute(query)
    rnoarray=cursor.fetchall()
    rno=map(lambda x:x[0],rnoarray)
    
    if str(rollno)in rno:
            fp=open(data.path+"/project_data/NewAppInter.html","r")
            web_page+=fp.read()
            
    else:
            fp=open(data.path+"/project_data/Newapplication.html","r")
            web_page+=fp.read()
     
    web_page2=open(data.path+"/project_data/student.html","r");
    web_page+=web_page2.read()

    web_page+="<table border=1 class=\"myTable\">"
    shownames=['RollNumber','Documents','Status']
    for i in shownames:
      web_page+="<th >%s </th>"%(i)    
    web_page+="<tr>"
    for i in range(len(names)):
	web_page+="<td><input ng-model=\"ch.%s\" placeholder=%s></td>"%(names[i],shownames[i]) 
    
    web_page+="</tr>"
    web_page+="<tr style=\"width:100px;\" ng-repeat=\"chrp in chiarperson|filter:ch|filter:statuspa|filter:fname\">"
    
    lnt=len(names);
    
                         
    for n in range(0,len(names)):
                               	 web_page+="<td>{{chrp.%s}}"%(names[n]);
                                 
                                 if names[n]=="Status%s"%(rollno):
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Filled\' && (chrp.Documents%s!=\'Fee Structure Certificate For Bank\' && chrp.Documents%s!=\'International Bonafide Certificate\' && chrp.Documents%s!=\'No Dues Certificate\')\"></form><form value=\"form\" action=\"read_pur.py\" method=\"post\"><input type=hidden name=\'edit\' value={{chrp.Documents%s}}><input type=hidden name=\"e\" value=1><input type=submit value=Edit></form><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=hidden name=\'prps\' value={{chrp.Documents%s}}><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"0\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=hidden name=\'prps\' value={{chrp.Documents%s}}><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APBN\"></form></td>"%(rollno,rollno,rollno,rollno,rollno,rollno,rollno)
                                   
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Filled\' && chrp.Documents%s==\'Fee Structure Certificate For Bank\'\"></form><form value=\"form\" action=\"read_bank.py\" method=\"post\"><input type=hidden name=\"edit\" value=1><input type=submit value=Edit></form><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"2\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APFS\"></form></td>"%(rollno,rollno) 
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Filled\' && chrp.Documents%s==\'No Dues Certificate\'\"><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"1\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APND\"></form></td>"%(rollno,rollno)
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Filled\' && chrp.Documents%s==\'International Bonafide Certificate\'\"><form value=\"form\" action=\"st_loh.py/print_Application_stud\" method=\"post\"><input type=submit value=Submit><input type=hidden name=\"ff\" value=\"3\"></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APIB\"></form></td>"%(rollno,rollno)
                                   
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Partially Filled\' && chrp.Documents%s==\'Bonafide Certificate\'\"><form value=\"form\" action=\"read_pur.py\" method=\"post\"><input type=submit value=Edit></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=hidden name=\'prps\' value={{chrp.Documents%s}}><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APBN\"></form></td>"%(rollno,rollno,rollno)
                                   
                                   web_page+="<td ng-if=\"chrp.Status%s==\'Application Form Partially Filled\' && chrp.Documents==\'Fee Structure Certificate For Bank\'\"><form value=\"form\" action=\"read_bank.py\" method=\"post\"><input type=submit value=Edit><input type=hidden name=\"edit\" value=1></form><form value=\"form\" action=\"./delete.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"appid\" value=\"APFS\"></form></td>"
                                   return """<html>%s</html>"""%(web_page)
                       
def print_Application_stud(req):
           
           session = Session.Session(req);
           Rollno=session['rno']
           ip=session['ipaddr']
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
           
           ff=int(info['ff'])
           if ff==0:
           	prps=info['prps']
	        
                prps=prps.split('Bonafide Certificate For')[1].strip()
           else:
		prps=''
           arrayid=["APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,%s"%(prps),"APND,ApplicationFormFilled,ApplicationSubmitted,No Dues Certificate,apply for No Dues Certificate"
,"APFS,ApplicationFormFilled,ApplicationSubmitted,Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","APIB,ApplicationFormFilled,ApplicationSubmitted,International Bonafide Certificate,apply for International Bonafide Certificate","APBN,ApplicationFormFilled,ApplicationSubmitted,Bonafide Certificate,apply for Bonafide Certificate"]
           
           psid=arrayid[ff]
           appid=psid.split(',')[0]
           aplydc=psid.split(',');
           aplydc=aplydc[3:]
           	
           query="""select fromState,toState from applicationProcess.requestStateTransitions where userId=%s and params like %s;"""
           cursor.execute(query,(Rollno,appid+'%'))
           val=cursor.fetchall()
           states=val[len(val)-1]
           
           if states==('ApplicationFormFilled','ApplicationFormPartiallyFilled'):
           	 flg=1
                 apl=','.join(applydc)
	  	 query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""
                 
                 cursor.execute(query,(Rollno,tabid,iplog,appid+",ApplicationFormFilled,ApplicationFormFilled,"+apl))
         	 db.commit();




           query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values (NOW(),"insert",%s,%s,%s,%s);"""
           cursor.execute(query,(Rollno,tabid,ip,psid))
       	   db.commit();
           
           
           fp=open(data.path+"/project_data/autoclick4.html")
           fp=fp.read()   
           return fp

