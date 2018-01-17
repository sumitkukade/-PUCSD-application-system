import MySQLdb
import re
from subprocess import call
from config_path import data
from mod_python import Session
sname=0
def split_uppercase(s):
            return re.sub(r'([^A-Z])([A-Z])', r'\1 \2',s)

def index(req):
    
    global sname
    session = Session.Session(req)
    session['prps']=''
    session.save()
    session.load()
    session.cleanup()
    
    try:
       sname=session['sno'];
    except:
           return """<html>Session Expired<p><a href="../staff_log.html"> LOGIN AGAIN</a></html>"""
    ip=session['ipaddr']
    info=req.form
    
    try:
        loop=info['pgs'];
        session['loop']=loop
	session.save()
    except:
        loop=session['loop']
    

    count=int(session['cnt'])+1;
    req.content_type="text/html"
    file=open(data.path+"/project_data/nevtag.html","r");
    file=file.read()
    req.write(file)
    req.write("<title>"+sname+"</title>")
    	
    web_page=""
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    #table="""create table staffTable (RollNo int,Document varchar(50),status varchar(50));""";
    #cursor.execute(table);
    
    query="""select appDesc from applicationProcess.applicationDomain """
    cursor.execute(query);
    query_result=cursor.fetchall()
    appname=map(lambda x:x[0],query_result) 
    
   

    
    cursor.execute("""select  appId  from  applicationProcess.applicationDomain ;""");   
    appid=cursor.fetchall()
    appid=map(lambda x:x[0],appid)
   

     
       
    cursor.execute("""select  userId,remark,applicationPurpose from  applicationProcess.requestStateTransitions where toState= 'ApplicationSubmitted';""");   
    query_result=cursor.fetchall()

    query_result=map(lambda x:x,query_result)
    newA=query_result
     
    
    result=[]
    application_name=['Bonafide Certificate','Fee Structure Certificate For Bank','International Bonafide Certificate','No Dues Certificate']
    
   
    arrayid=["Bonafide Certificate,apply for Bonafide Certificate","Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]

    cursor.execute("""select  userId,remark,applicationPurpose from  applicationProcess.requestStateTransitions where toState= 'RequestArrivedInOffice';""");   
    rquery_result=cursor.fetchall()
    rquery_result=map(lambda x:x,rquery_result)
    
    	
    
    	
    for i in range(0,len(newA)):
      
      query="""select  * from  applicationProcess.requestStateTransitions where userId=%s and remark=%s order by requestId desc limit 1 ;"""
      cursor.execute(query,(str(query_result[i][0]),str(query_result[i][1])));
      query_result1=cursor.fetchall()
      query_result1=map(lambda x:x,query_result1[0])
      result.append(query_result1)
    d=6;
       
    for Rno,cname,purps in query_result[(len(rquery_result)):]:
            
            if  cname=='Bonafide Certificate':
	                 purps=purps.strip()
            		             
                         qr="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",ApplicationSubmitted,RequestArrivedInOffice,"%s","%s","%s);"""
    			         
                         cursor.execute(qr,(sname,str(ip),appid[application_name.index(cname)],Rno,cname,purps));
                         db.commit()
                         
            else:
                         
                         qr="""insert into inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s",ApplicationSubmitted,RequestArrivedInOffice,"%s","%s);"""
                         
                         cursor.execute(qr,(sname,str(ip),appid[application_name.index(cname)],Rno,arrayid[application_name.index(cname)]));
                         db.commit()
            
                         
            q4 = """select msg from userInputDatabase.outputErrorMsgs where requestId = (select requestId from userInputDatabase.inputRequests where userId=%s  order by requestId desc limit 1);"""       
             
            cursor.execute(q4,(sname,))
            res = cursor.fetchall()
            if len(res)!=0:
             
         	return """</form><html>%s <form value="form" action="#" method="post"><input type=\"submit\"value=\"OK\"></form></html>"""%(res[0])
            

    query="""DROP TABLE IF EXISTS userInputDatabase.staffTable;""";
    cursor.execute(query);
    db.commit()

    table="""create table userInputDatabase.staffTable(RollNo int,Ref_No text, Document text,status text);""";
    cursor.execute(table);
    db.commit()   
    
    newA.reverse()
    
    for Rno,cname,purps in (newA):
                if cname=='Bonafide Certificate': 
    			     
                            query="""select toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s and applicationPurpose=%s   order by requestId desc limit 1 ;"""   
                            cursor.execute(query,(Rno,appid[application_name.index(cname)],purps));   
                            re=cursor.fetchall()
                           
                            re=map(lambda x:x,re)
                            state=split_uppercase(re[0][0])
                               
                            query="""select refNo from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s and applicationPurpose=%s;"""
                            
                           
                            cursor.execute(query,(Rno,appid[application_name.index(cname)],purps));   
                            ref_no=cursor.fetchall()
                            ref_no=map(lambda x:x[0],ref_no)
                            
                            if len(ref_no)==0:
                                        ref_no=''
                            else:
                                        ref_no=ref_no[0]
                                        
                                        
                            if len(re)!=0:
                                        re=map(lambda x:x[0],re)
					
                                        query="""insert into userInputDatabase.staffTable values(%s,%s,%s,%s)"""
                                        cursor.execute(query,(Rno,"CSD/"+str(ref_no),cname+" For "+purps,state))
                                        db.commit();
     			    
                else:
			    
                            query="""select toState from applicationProcess.aux_studentAndState where rollNumber=%s and appId=%s   order by requestId desc limit 1 ;"""   
                            cursor.execute(query,(Rno,appid[application_name.index(cname)]));   
                            re=cursor.fetchall()
                            re=map(lambda x:x,re)
                            state=split_uppercase(re[0][0])
                            
                            query="""select refNo from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""
                            
                            
                            cursor.execute(query,(Rno,appid[application_name.index(cname)]));   
                            ref_no=cursor.fetchall()
                            ref_no=map(lambda x:x[0],ref_no)
                            
                            if len(ref_no)==0:
                                        ref_no=''
                            else:
                                        ref_no=ref_no[0]
                                        
                                        
                            if len(re)!=0:
                                        re=map(lambda x:x[0],re)
                                        query="""insert into userInputDatabase.staffTable values(%s,%s,%s,%s)"""
                                        cursor.execute(query,(Rno,"CSD/"+str(ref_no),cname,state))
                                        db.commit();
     






                            
    fp1=open(data.path+"/project_data/json.txt","w");
    fp1.write("[");
    
    cursor.execute(""" select * from userInputDatabase.staffTable limit %s offset %s; """%(int(data.sizeforpage)+1,loop));
    query_resultall=cursor.fetchall()
    
    cursor.execute(""" select * from userInputDatabase.staffTable limit %s,%s;"""%(loop,int(data.sizeforpage)));
    query_result=cursor.fetchall()
    
    names = list(map(lambda x: x[0], cursor.description))  
    
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
         
    fp2=open(data.path+"/project_data/json1.txt","w");
    fp2.write("[");
    
    for n in range(0,len(names)):
                fp2.write("{");
                if n==len(names)-1:
                    fp2.write("count:0}");	
		else:	
		 fp2.write("count:0},");	

    fp2.write("]");
    	
    #web_page+="""</form><form align=right method="post" action="search-data-in-table.py"><input type="submit" value="Rejected Student List"></form><p>"""
    #web_page+="""</form><form method="post" action="search-data-in-table1.py"><input type="submit" value="Certificate Collected Student List"></form><hr>"""
    	
    crp=open(data.path+"/project_data/sample.html","r");
    web_page+=crp.read()
    
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
    
    
    
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="mysql" )
    db.close()



   
    query1="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='ApplicationRejectedByOffice'""";
    cursor.execute(query1)
    query_result=cursor.fetchall()
    query_result= map(lambda x:str(x[0]),query_result)
    a=split_uppercase(query_result[0])
    b=split_uppercase(query_result[1])
    query_result=[]
    query_result.append(a)
    query_result.append(b)
    
    query2="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='ApplicationSubmitted'""";
    cursor.execute(query2)
    query_result2=cursor.fetchall()
    query_result2= map(lambda x:str(x[0]),query_result2)
    a=split_uppercase(query_result2[0])
    query_result2=[]
    query_result2.append(a)
    
    query3="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='FormPrinted'""";
    cursor.execute(query3)
    query_result3=cursor.fetchall()
    query_result3= map(lambda x:str(x[0]),query_result3)
    a=split_uppercase(query_result3[0])
    b=split_uppercase(query_result3[1])
    e=split_uppercase(query_result3[2])
    query_result3=[]
    query_result3.append(a)
    query_result3.append(b)
    query_result3.append(e)
    
    query4="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='ApplicationModification'""";
    cursor.execute(query4)
    query_result4=cursor.fetchall()
    query_result4= map(lambda x:str(x[0]),query_result4)
    a=split_uppercase(query_result4[0])
    b=split_uppercase(query_result4[1])
    query_result4=[]
    query_result4.append(a)
    query_result4.append(b)

    query5="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='FormSigned'""";
    cursor.execute(query5)
    query_result5=cursor.fetchall()
    query_result5= map(lambda x:str(x[0]),query_result5)
    a=split_uppercase(query_result5[0])
    b=split_uppercase(query_result5[1])
    e=split_uppercase(query_result5[2])
    query_result5=[]
    query_result5.append(a)
    query_result5.append(b)
    query_result5.append(e)
    try:
      query_result5.remove('Form Printed')
    except:
           a="ok"
   
    query6="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='CertificateCollectedByStudent'""";
    cursor.execute(query6)
    query_result6=cursor.fetchall()
    query_result6= map(lambda x:str(x[0]),query_result6)
    a=split_uppercase(query_result6[0])
    query_result6=[]
    query_result6.append(a)
    
    query7="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='RequestArrivedInOffice'""";
    cursor.execute(query7)
    query_result7=cursor.fetchall()
    query_result7= map(lambda x:str(x[0]),query_result7)
    a=split_uppercase(query_result7[0])
    b=split_uppercase(query_result7[1])
    e=split_uppercase(query_result7[2])
    query_result7=[]
    query_result7.append(a)
    query_result7.append(b)
    query_result7.append(e)
    	
    try:
      query_result7.remove('Form Printed')
      query_result7.remove('Application Modification');
    except:
           a="ok"
   

    query8="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='RequestFinishedSuccessfully'""";
    cursor.execute(query8)
    query_result8=cursor.fetchall()
    query_result8= map(lambda x:str(x[0]),query_result8)
    a=split_uppercase(query_result8[0]) 
    query_result8=[]
    query_result8.append(a)
    
    query9="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='SignedFormArrivedInOffice'""";
    cursor.execute(query9)
    query_result9=cursor.fetchall()
    query_result9= map(lambda x:str(x[0]),query_result9)
    a=split_uppercase(query_result9[0])
    b=split_uppercase(query_result9[1])
    e=split_uppercase(query_result9[2])
    query_result9=[]
    query_result9.append(a)
    query_result9.append(b)
    query_result9.append(e)
    query10="""select staffActionTo from applicationProcess.staffActionDomain where staffActionFrom='ModificationSuccessfully'""";
    cursor.execute(query10)
    query_result10=cursor.fetchall()
    query_result10= map(lambda x:str(x[0]),query_result10)
    a=split_uppercase(query_result10[0])
    b=split_uppercase(query_result10[1])
    query_result10=[]
    query_result10.append(a)
    query_result10.append(b)
      

    web_page+="""<p>NEW REQUEST<input type=checkbox ng-model=\'chkk\'><span ng-if=\"chkk==true\" ng-init="change()"></span><span ng-if=\"chkk==false\" ng-init="change1()"></span>"""
    #web_page+="""<label ></label>Select All<input type=\"checkbox\" ng-model=\"all\"> """	
    

	
    web_page+="<table border=1  class=\"myTable\"><tr>"
    
    for i in names:
      web_page+="<th textcolor=\"black\">%s</th>"%(i)
    web_page+=("""<th></form><form  method="post" action="./newprint.py"><input type=hidden value={{all}} name=\"all\"><input type=hidden value={{items}} name=\"printarray\"><input type=\"submit\" value=\"Download zip\"></form></div></html><th>""");
    
    web_page+="</tr>"
    for i in names:
        if i=='RollNo' or i=="Ref_No":
		web_page+="<td style=\"width:10px;\"><input style=\"width:120px;\"  ng-model=\"ch.%s\" placeholder=\"search %s\"></td>"%(i,i) 
        else:	
		web_page+="<td style=\"width:10px;\"><input ng-model=\"ch.%s\" placeholder=\"search %s\"></td>"%(i,i) 
    web_page+="""<td input >Select All &nbsp<input type=\"checkbox\" ng-model=\"all\"></td>"""
    web_page+="</tr>"
    web_page+="<tr\" ng-repeat=\"chrp in chiarperson|filter:ch|filter:statuspa|filter:fname\">"

    
    web_page+="<tr ng-repeat=\"chrp in chiarperson|filter:ch|filter:fname|filter:chk\"><p>"
    lnt=len(names);
   
   
    ss=""

    ll	="""select status from userInputDatabase.staffTable;"""
    cursor.execute(ll)
    aps=cursor.fetchall()
    aps=map(lambda x:x[0],aps);

    
 
    allre="""SELECT count(*) FROM  applicationProcess.studentApplicationQueue""";
    cursor.execute(allre)
    allre=cursor.fetchall();
    
    if allre[0][0]!=0:
       allre=allre[0][0]
    else:
         allre=1;
    #web_page+="<label>Check me to check both: <input type=\"checkbox\" ng-model=\"leader\"></label><br/>" 

    
    query="""Select * from applicationProcess.studentApplicationQueue order by requestId  limit %s,1;"""%(str(count%allre))
    
    cursor.execute(query);
    
    que=cursor.fetchall()
    
    qrl='';
    qid='';
    if len(que)!=0:
        que=que[0]
        qrl=que[1]
        qid=que[2]
    
    
    query="""Select appDesc from applicationProcess.applicationDomain where appId='%s';"""%(str(qid));
    cursor.execute(query);
    qdc=cursor.fetchall()
    if len(qdc)!=0:
        qdc=qdc[0][0]
    else:
        qdc=''
    
    
        
    if (int(loop)-1)>=0:         
		web_page+=("""<div class=\"inner\"></form><html><form method="post" action="./log_staff.py"><input type=hidden value='%s' name='pgs'><input type="submit" value=&laquo;prev></form></html></div>&nbsp&nbsp"""%(int(loop)-int(data.sizeforpage)))
   	
    if len(query_resultall)>(int(data.sizeforpage)):
 	web_page+=("""</form><html><div class=\"inner\"><form method="post" action="./log_staff.py"><input type=hidden value='%s' name='pgs'><input type="submit" value=next&raquo;></form></div></html>"""%((int(loop)+int(data.sizeforpage))));
    try:
    	p=int(loop)/int(data.sizeforpage)
    except:
	p=0;
    web_page+="""<p>Page No:%s"""%(p) 
    for n in range(0,lnt):
      if names[n]=='RollNo' or names[n]=='Ref_No':
      	  web_page+="<td style=\"width:10px;\">{{chrp.%s}}</td>"%(names[n]);
      else:	
        web_page+="<td>{{chrp.%s}}</td>"%(names[n]);
    

      cnt=1;
      
      if('status' in names[n]):
        enb=''      			
    	web_page+="<td ng-if=\"chrp.%s ==\'Application Rejected By Office\'\" ng-init=\"ststs2=%s\">"%(names[n],query_result)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"> Remark<input type=\"text\" name=\"rmk\"> <input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select   name=\"sopt\" ng-model=\"stats2\" name=''ng-options=\"op for op in ststs2\"></select>"%(query_result)
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
	
        
        
        web_page+="</td>"  





        web_page+="<td  ng-if=\"chrp.%s ==\'Application Submitted\'\" ng-init=\"ststs3=%s\">"%(names[n],query_result2)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats3\" name=''ng-options=\"op for op in ststs3\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td>"  
	
	
            
        web_page+="<td ng-if=\"chrp.%s ==\'Form Printed\'\" ng-init=\"ststs4=%s\">"%(names[n],query_result3)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select %s name=\"sopt\" ng-model=\"stats4\" name=''ng-options=\"op for op in ststs4\"> </select>"%(enb)
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td><div>" 
	web_page+="<td ng-if=\"chrp.%s ==\'Form Printed\'\" ng-init=\"ststs4=%s\">"%(names[n],query_result3)                        
        web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
        web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""


        web_page+="<td ng-if=\"chrp.%s ==\'Application Modification\'\" ng-init=\"ststs12=%s\">"%(names[n],query_result4)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats12\" name=''ng-options=\"op for op in ststs12\"> </select>"
        fp=open(data.path+"/project_data/nn.html")

        web_page+=fp.read();
        web_page+="<form value=\"form\" action=\"refno.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><input type=submit value=EDIT></form>"  

	web_page+="<td ng-if=\"chrp.%s ==\'Application Modification\'\" ng-init=\"ststs5=%s\">"%(names[n],query_result5)                        
	web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
    	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""




        
      
        web_page+="<td ng-if=\"chrp.%s ==\'Form Signed\'\" ng-init=\"ststs5=%s\">"%(names[n],query_result5)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats5\" name=''ng-options=\"op for op in ststs5\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td>"  
        
	web_page+="<td ng-if=\"chrp.%s ==\'Form Signed\'\" ng-init=\"ststs5=%s\">"%(names[n],query_result5)                        
	web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
    	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""

 


        web_page+="<td ng-if=\"chrp.%s ==\'Certificate Collected By Student\'\" ng-init=\"ststs6=%s\">"%(names[n],query_result6)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats6\" name=''ng-options=\"op for op in ststs6\"></select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td>"
	web_page+="<td ng-if=\"chrp.%s ==\'Certificate Collected By Student\'\" ng-init=\"ststs6=%s\">"%(names[n],query_result6)                        
   
        web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""




        web_page+="<td  ng-if=\"chrp.%s ==\'Request Arrived In Office\'\" ng-init=\"ststs7=%s\">"%(names[n],query_result7)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  %s name='sopt' ng-model=\"stats7\" ng-options=\"op for op in ststs7\">"%(enb)
        fp=open(data.path+"/project_data/nn.html")

        web_page+=fp.read();
        web_page+="<form value=\"form\" action=\"refno.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><input type=submit value=EDIT></form></td>"  
        


        web_page+="<td ng-if=\"chrp.%s ==\'Request Finished Successfully\' || chrp.%s ==\'Request Fisnished With Error\' \" ng-init=\"ststs8=%s\">"%(names[n],names[n],query_result8)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats8\" name=''ng-options=\"op for op in ststs8\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td>"
	web_page+="<td ng-if=\"chrp.%s ==\'Request Finished Successfully\' || chrp.%s ==\'Request Fisnished With Error\' \" ng-init=\"ststs8=%s\">"%(names[n],names[n],query_result8)   
	web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""


        


        web_page+="<td ng-if=\"chrp.%s ==\'Signed Form Arrived In Office\'\" ng-init=\"ststs9=%s\">"%(names[n],query_result9)                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats9\" name=''ng-options=\"op for op in ststs9\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="</td>"
	web_page+="<td ng-if=\"chrp.%s ==\'Signed Form Arrived In Office\'\" ng-init=\"ststs9=%s\">"%(names[n],query_result9)                        
	
	web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""

  
        

        


    

        web_page+="<td ng-if=\"chrp.%s ==\'Modification Successfully\' \" ng-init=\"ststs10=%s\">"%(names[n],query_result10)
                        
    	web_page+="</form><html><head><body><form value=\"form\" action=\"log_staff.py/okfun\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}></lable><select  name=\"sopt\" ng-model=\"stats10\" name=''ng-options=\"op for op in ststs10\"> </select>"
        
        fp=open(data.path+"/project_data/nn.html")
        web_page+=fp.read();
        web_page+="<span class=\"in\"><form value=\"form\" action=\"pdf.py\" method=\"post\"><input type=hidden name=\"rono\" value={{chrp.RollNo}}><input type=hidden name=\"docm\" value={{chrp.Document}}><input type=submit value=PRINT></form></div></td>"
	web_page+="<td ng-if=\"chrp.%s ==\'Modification Successfully\' \" ng-init=\"ststs10=%s\">"%(names[n],query_result10)
	web_page+="""<input type=\"checkbox\" ng-checked=\"all\" ng-model=s1>
		<div ng-if="s1==true" ng-init="addToCart(chrp.RollNo+'&'+chrp.Document)"></div>"""
	web_page+="""<div ng-if="s1==false" ng-init="removeToCart(chrp.RollNo+'&'+chrp.Document)"></div></td>"""

  
	      #web_page+="<td><input id=\"checkFollower\" ng-model=\"leader\" type=\"checkbox\" ng-checked=\"leader\" aria-label=\"Follower input \">{{leader}}</td>"
	
         
    #web_page+="<td>{{stats}}<td>"
      
    return """<html>%s</html>"""%(web_page)
    
def okfun(req):

   session = Session.Session(req)
   session.load()	
   sname=session['sno']
   ip=session['ipaddr']
   
   info = req.form
   info=req.form
   rolno=info['rono']
   
   docm=info['docm']
   docm1=info['docm']
   stt=info['sopt']
   if len(stt)==0 or len(stt)==1:
           fp=open(data.path+"/project_data/autoclick3.html")
           fp=fp.read()   
           return fp
   db = MySQLdb.connect(
   host="localhost",
   user=data.mysql_user,
   passwd=data.mysql_pswd,
   db="userInputDatabase" )
   cursor = db.cursor()
   try:
               if "Bonafide Certificate For" in docm:
               		docm=docm.split('For')
	      		docm=docm[0].strip()
               		edit=docm1.split('Bonafide Certificate For')
	       		edit=edit[1].strip()
	       else:
			edit=''
   except:
               docm=docm
               edit='';
  
   query="""select  appId from applicationProcess.applicationDomain where appDesc='%s';"""%(docm)
   cursor.execute(query)   
   query_result=cursor.fetchall()
   
   query_result=map(lambda x:x[0],query_result)
  
   query="""select status  from staffTable where RollNo=%s and Document= %s;""";
   cursor.execute(query,(rolno,docm1))   
   sts=cursor.fetchall()
   
   
   sts=map(lambda x:x[0],sts)[0]
   sts=sts.replace(" ", "")
     
   stt=stt.replace("string:","").strip()
   stt=stt.replace(" ", "")
   
   arrayid=["Bonafide Certificate,%s"%(edit),"Fee Structure Certificate For Bank,apply for Fee Structure Certificate For Bank","International Bonafide Certificate,apply for International Bonafide Certificate","No Dues Certificate,apply for No Dues Certificate"]
   for i in arrayid:
        if docm in i:
           
           if stt=='FormPrinted':

                if docm=='International Bonafide Certificate':
                    filename="""%s_International_bonafide.pdf"""%(rolno);
                elif docm in 'Bonafide Certificate For':
                    filename="""%s_Bonafide_For_%s.pdf"""%(rolno,edit)
                elif docm=='Fee Structure Certificate For Bank':
                     filename="""%s_feestructure.pdf"""%(rolno);
                elif docm=='No Dues Certificate':
                      filename="%s_No_Dues.pdf"%(rolno)
                
		try:
	 		s1=open(data.path+'/project_data/doc_pdf/'+filename,"r");
                except:
                	return """<html><html><link rel="stylesheet" href="../code.css"/><ul><li><a  class="active"  href="../st_loh.py">HOME</a></li><li style="float:right"><a href="../logout.py">LOGOUT</a></li></ul><br><b>FIRSTLY PRINT FORM</b><p><form method="post" action="../log_staff.py"><input type="submit" value="Back"></form></html>""";
                
		s1=s1.read()
                
		db = MySQLdb.connect(
		host="localhost",
		user=data.mysql_user,
		passwd=data.mysql_pswd,
		db="userInputDatabase")
		cursor = db.cursor();
                

                
                query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,applicationPdf,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s,%s);"""
                
                cursor.execute(query,(sname,ip,s1,(query_result[0]+","+sts+","+stt+","+rolno+","+i)))

                    

   
           elif sts=='ApplicationModification' and stt=='ApplicationRejectedByOffice':
 
                          mds2="""%s,ApplicationModification,ApplicationRejectedByOffice,%s,%s);"""%(query_result[0],rolno,i);
                          sd2="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s);"""
                          cursor.execute(sd2,(sname,mds2))
                          db.commit()
  
           elif 'CertificateCollectedByStudent'==sts:
                
                 
                 query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
                 cursor.execute(query,(sname,ip,(query_result[0]+","+sts+","+stt+','+rolno+','+i)));
           elif sts=="ApplicationRejectedByOffice":
              remark=info['rmk'];
              query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
              nr=i.split(',');
              nr[0]=remark+',';
              nr=''.join(nr)
              
              cursor.execute(query,(sname,ip,(query_result[0]+","+sts+","+stt+','+rolno+','+nr)));
           elif 'ModificationSuccessfully'==stt:
                          mds="""%s,ApplicationModification,ModificationSuccessfully,%s,%s);"""%(query_result[0],rolno,i);
                          sd="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s);"""
                          cursor.execute(sd,(sname,mds))
                          db.commit()  
                
           else:
             query="""insert into userInputDatabase.inputRequests(requestTime,requestType,userId,tableId,iplog,params) values(NOW(),"insert",%s,"applicationRequestByStaff",%s,%s);"""
       
             cursor.execute(query,(sname,ip,(query_result[0]+","+sts+","+stt+","+rolno+','+i)))
             
           a=split_uppercase(stt)
           
           query="""update staffTable set status=%s where RollNo=%s and Document=%s;"""   
           cursor.execute(query,(a,rolno,docm));
           db.commit()
           session['cnt']=int(session['cnt'])+1
           session.save()
           
           fp=open(data.path+"/project_data/autoclick3.html")
           fp=fp.read()   
           return fp
