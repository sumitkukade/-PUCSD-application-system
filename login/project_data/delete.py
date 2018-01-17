import MySQLdb
from mod_python import Session
from config_path import data
def index(req):

    session = Session.Session(req)
    session.load()    
    
    try:
      rollno=session['rno']
    except:
       return """<html>Session Expired<p><a href="../student_login.html"> LOGIN AGAIN</a></html>"""
    
    
    req.content_type = 'text/html'
    #req.write('rollno: %s\n' % session['rno'])

    crpn=""
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    info = req.form
    apid = info["appid"]
    cursor = db.cursor() 

    if apid=='APBN':
	edit =info['prps']
	edit=edit.split('Bonafide Certificate For')
	edit=edit[1].strip()
	
   	q1 = """delete from userInputDatabase.inputRequests where requestId = (select requestId from applicationProcess.applicationForm where rollNumber=%s and appId=%s and applicationPurpose=%s order by requestId desc limit 1 );"""
    	cursor.execute(q1,(rollno,apid,edit))
    	db.commit()
	q2 = """delete from applicationProcess.applicationForm where rollNumber=%s and appId=%s and applicationPurpose=%s;"""
   	cursor.execute(q2,(rollno,apid,edit))
	db.commit()
	q3 = """delete from userInputDatabase.inputRequests where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s and applicationPurpose=%s);"""
        cursor.execute(q3,(rollno,apid,edit))
        db.commit()


	q4 = """delete from userInputDatabase.outputErrorMsgs where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s and applicationPurpose=%s);"""
	cursor.execute(q4,(rollno,apid,edit))
        db.commit()

        q5 = """delete from userInputDatabase.outputResults where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s and applicationPurpose=%s);"""
        cursor.execute(q5,(rollno,apid,edit))
        db.commit()

        q6 = """delete from applicationProcess.requestStateTransitions where requestId in(select requestId from applicationProcess.applicationRequests where userId=%s and appid=%s and applicationPurpose=%s);"""
        cursor.execute(q6,(rollno,apid,edit))
        db.commit()
    
        q7 = """delete from applicationProcess.aux_requestStateTransitions where requestId in(select requestId from applicationProcess.applicationRequests  where userId=%s and appid=%s and applicationPurpose=%s);"""
        cursor.execute(q7,(rollno,apid,edit))
        db.commit() 
    
        q8 = """delete from applicationProcess.applicationRequests where userId=%s and appId=%s and applicationPurpose=%s;"""
        cursor.execute(q8,(rollno,apid,edit))
        db.commit()
   











    else:
	q1 = """delete from userInputDatabase.inputRequests where requestId = (select requestId from applicationProcess.applicationForm where rollNumber=%s and appId=%s);"""
    	cursor.execute(q1,(rollno,apid))
    	db.commit()
	
	
        if(apid=='APFS'):
            q9 = """delete from applicationProcess.feesStructureForm where rollNumber = (select rollNumber from applicationProcess.applicationForm where rollNumber = %s and appId= %s);"""
            cursor.execute(q9,(rollno,apid))
            db.commit()

        q2 = """delete from applicationProcess.applicationForm where rollNumber=%s and appId=%s;"""
        cursor.execute(q2,(rollno,apid))
        db.commit()

        q3 = """delete from userInputDatabase.inputRequests where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s);"""
        cursor.execute(q3,(rollno,apid))
        db.commit()

        q4 = """delete from userInputDatabase.outputErrorMsgs where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s);"""
        cursor.execute(q4,(rollno,apid))
        db.commit()
        
        q5 = """delete from userInputDatabase.outputResults where requestId in (select requestId from applicationProcess.applicationRequests where userId=%s and appId=%s);"""
        cursor.execute(q5,(rollno,apid))
        db.commit()
        
        q6 = """delete from applicationProcess.requestStateTransitions where requestId in(select requestId from applicationProcess.applicationRequests where userId=%s and appid=%s);"""
        cursor.execute(q6,(rollno,apid))
        db.commit()
        
        q7 = """delete from applicationProcess.aux_requestStateTransitions where requestId in(select requestId from applicationProcess.applicationRequests  where userId=%s and appid=%s);"""
        cursor.execute(q7,(rollno,apid))
        db.commit() 
    
        q8 = """delete from applicationProcess.applicationRequests where userId=%s and appId=%s;"""
        cursor.execute(q8,(rollno,apid))
        db.commit()
        
        
    fp=open(data.path+"/project_data/autoclick2.html")
    fp=fp.read()   
    return fp

    
