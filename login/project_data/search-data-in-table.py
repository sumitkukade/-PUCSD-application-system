import MySQLdb
import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session

def index():
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="applicationProcess" )
    cursor = db.cursor()
   
    ss="""select * from applicationProcess.applicationRejectRemark ;"""
    cursor.execute(ss)
    val=cursor.fetchall()
    # disconnect from server
    
    query="""DROP TABLE IF EXISTS rejectRemark;""";
    cursor.execute(query);
    db.commit()
    table="""create table rejectRemark(RollNumber int,appId text, Document text,Remark text);""";
    cursor.execute(table);
    
    for i in val:
        	ss="""insert into rejectRemark values(%s,%s,%s,%s)"""
                if i[2]=='APBN':
                     np="Bonafide Certificate FOR %s"%(i[4]);
                elif i[2]=="APFS":
                     np="FEES STRUCTURE";
                elif i[2]=="APND":
                     np="NO DUES";
                else:
                     np="INTERNATIONAL BONAFIDE"
                       
       		cursor.execute(ss,(i[1],i[2],np,i[3]))
       		db.commit();
        



    ss="""select * from rejectRemark ;"""
    cursor.execute(ss)
    val=cursor.fetchall()
    names = list(map(lambda x: x[0], cursor.description))
    fp1=open(data.path+"/project_data/json3.txt","w");
    fp1.write("[");
    for i in range(0,len(val)):
        fp1.write("{");
    	for n in range(0,len(names)):
		fp1.write("\""+str(names[n])+"\":");
		if str(val[i][n]).isdigit():
                	fp1.write(str(val[i][n]));
		else:
	                fp1.write("\""+str(val[i][n])+"\"");
		
		if not n==len(names)-1:
		  fp1.write(",\n");
	if not i==len(val)-1:
        	fp1.write("},\n");
	else:
		fp1.write("}	\n");
		

    fp1.write("]");

    crpn=open(data.path+"/project_data/sample1.html","r");
    crpn=crpn.read()
    crpn+="<table border=1 class=myTable>"

    for i in names:
      if i=="appId":
          continue;   
       

      crpn+="<th >%s</th>"%(i)
    crpn+="<tr>"
    for i in names:      
        if 'appId'==i:
             continue
	crpn+="<td><input ng-model=\"ch.%s\" placeholder=%s>"%(i,i) 
    crpn+="</tr>"    
    crpn+="<tr ng-repeat=\"chrp in chiarperson|filter:ch|filter:fname\">"
   
    for n in range(0,len(names)):
                                 if names[n]=='appId':
                                        continue;

                               	 crpn+="<td>{{chrp.%s}}</td>"%(names[n])
    crpn+="<td><form value=\"form\" action=\"./delete1.py\" method=\"post\"><input type=\"submit\" value=\"Delete\"><input type=\"hidden\" name=\"rono\" value={{chrp.RollNumber}}><input type=\"hidden\" name=\"apid\" value={{chrp.appId}}><input type=\"hidden\" name=\"prps\" value={{chrp.Remark}}></form></td>" 
    return """<html>%s</html>"""%(crpn)
