import MySQLdb
from subprocess import call
from config_path import data
from mod_python import Session
import zipfile
from config_path import data
from mod_python import Session
from config_path import data
import MySQLdb
import time;
import refno
from mod_python import Session
from config_path import data
import student
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
def addr_split(nn):
               cnt=0
               cntt=0
          
               nn=list(nn)
               for i in range(0,len(nn)):
                   if nn[i]==',':
                        nn[i]='\n';
                        cntt=1
                   elif nn[i]==' ':
                       cntt+=1;
                       if cntt%3==0:
                           nn[i]='\n';


               return nn;

def index(req):
    session = Session.Session(req)
    session.load()
    db = MySQLdb.connect(
    host="localhost",
    user=data.mysql_user,
    passwd=data.mysql_pswd,
    db="userInputDatabase" )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare a cursor object using cursor() method
    cursor = db.cursor();
    ss="""select  rollnumber,appId,applicationPurpose from applicationProcess.studentApplicationQueue where toState='RequestArrivedInOffice' order by requestId desc limit %s,%s;"""%(session['loop'],int(data.sizeforpage))

    cursor.execute(ss);
    rs=cursor.fetchall();
    addrs=[]
    
    for i in rs:
	 if i[1]=='APBN':
 	 	 ss="""select RollNumber,appId,applicationPurpose from applicationProcess.studentApplicationQueue where toState="ModificationSuccessfully" and rollnumber=%s and appId='%s' and applicationPurpose='%s' order by requestId desc limit 1;"""%(i[0],i[1],i[2])
		    
	   	 cursor.execute(ss);
	    	 result=cursor.fetchall();
		 result=map(lambda x:x,result)
         else:
  		 ss="""select RollNumber,appId,applicationPurpose from applicationProcess.studentApplicationQueue where toState="ModificationSuccessfully" and rollnumber=%s and appId='%s' order by requestId desc limit 1;"""%(i[0],i[1])
		    
	   	 cursor.execute(ss);
	    	 result=cursor.fetchall();
	 
	 if len(result)!=0:
		addrs.append(result[0])
    
    rs=addrs
    info=req.form
    printarray=info['printarray'];
    all1=info['all']
        	
    if(all1=="true") :
	
	rs=rs
    else:
		
	p=printarray.replace('[',"");
	p=p.replace(']','')
	p=p.replace("\"",'')
	p=p.split(",");
	p=map(lambda x:x.split('&'),p)
	
	
	
	if printarray=='[]':
		p=[]
	p1=p
	for i in p:
		
		if "Bonafide Certificate For" in i[1]:
			 
			 i=i.insert(1,"APBN")		
		else:
			ss="""select appId from applicationProcess. applicationDomain where appDesc='%s'"""%(i[1]);
			cursor.execute(ss);
			sss=cursor.fetchall()
			sss=map(lambda x:x[0],sss)
	
			i=i.insert(1,sss[0])
        for i in p:
		if "Bonafide Certificate For" in i[2]:
	       		 edit=i[2]
			 edit=edit.split('Bonafide Certificate For')
		         edit=edit[1].strip()
                         i=i.insert(2,edit)
		
      
	rs=p
    
    flall=[]
    zf = zipfile.ZipFile(data.path+'/project_data/doc_pdf/ALL_DOCUMENTS.zip', mode='w')
    fa=[];
    

    chrept=[]
    
    for i in rs:
    
         try:
                        Rollno=i[0]
         except:
                        return """<html><b>PRINT FORM Again</b><form method="post" action="./log_staff.py"><input type="submit" value="Back"></form></html>""";
         app=i[1]
         


         doc="";
         db = MySQLdb.connect(
    	 host="localhost",
    	 user=data.mysql_user,
    	 passwd=data.mysql_pswd,
    	 db="applicationProcess")

         cursor = db.cursor()
         
         ss= """select refNo from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""
         cursor.execute(ss,(Rollno,app))
         refn=cursor.fetchall(); 
         refn= map(lambda x:x[0],refn)[0]
         d=time.strftime("%d/%m/%Y")
         if app=='APBN':         

         
	 	ss="""select * from  studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 	cursor.execute(ss)
       	 	val=cursor.fetchall()
         
         	y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
         	cursor.execute(y,(Rollno,Rollno))
         	val1=cursor.fetchall()
         	yy= map(lambda x:x[0],val1)
         	
         	year=int(d.split('/')[2])
                
         	p="""select applicationPurpose from applicationForm where appId=%s and rollnumber=%s and applicationPurpose=%s;"""
         	cursor.execute(p,(app,Rollno,i[2]))
         	val2=cursor.fetchall()
         	purpose= map(lambda x:x[0],val2)[0]
                

         
         	ss= """select * from applicationProcess.applicationFormForStaff where rollNumber=%s and appId=%s;"""
         	cursor.execute(ss,(Rollno,app))
         	valu=cursor.fetchall(); 
		refn=map(lambda x:x,valu)[0][4]
         

         	
         	dat=str(time.strftime("%d/%m/%Y"));         

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
         	if (cnm[0]=='MCA' or cnm[0]=='mca'):
             		cname='Master of Computer Applications' 
             
         	else:
             		cname='Master of Computer Science'
                dt="""select  dateOfBirth from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
         	cursor.execute(dt)
         	valdt=cursor.fetchall()    
       		bdt= map(lambda x:x[0],valdt)
        	dtt=str(bdt[0]).split('-')
         	dtt.reverse()
         	dtt='-'.join(dtt)
                sss4="""select * from applicationProcess.officeContactDetails;"""
    	 	cursor.execute(sss4)
       	 	vall4=cursor.fetchall()
         	email_phone = map(lambda x:x,vall4)  

                filename="%s_Bonafide_For_%s.pdf"%(Rollno,purpose)
                doc12 = SimpleDocTemplate(data.path+"/project_data/doc_pdf/"+filename,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
	        Story=[]
	        magName = "Pythonista"
                logo = data.path+"/project_data/logo.jpg"
	        im = Image(logo, 1*inch, 1*inch)
                rno=refn
                dt=dat
                g=gen
                fn = val[0][4].upper()
                mn = val[0][5].upper() 
                ln = val[0][6].upper()
                rollno=Rollno
                cource=cname
                
                year=val[0][2]
                
                dt1=dt.split("/");
               
                if dt1[1]>5:
                   year1=str(dt1[2])+'-'+str(int(dt1[2])+1)
                else:
			year1=str(int(dt1[2])-1)+'-'+str(dt[2])	
                
                on_print_gender=hh
   
                addl1=val[0][12].title()
                addl2=val[0][13].title()
                addl3=val[0][14].title()
                date=dtt
	        formatted_time = time.ctime()
	        styles=getSampleStyleSheet()
	        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	        deptnm='DEPARTMENT OF COMPUTER SCIENCE'
	        ptext = '<para alignment=\'center\'><html><font size=20>%s</font></html></para>' % deptnm
	        Story.append(Paragraph(ptext, styles["Normal"]))
	        Story.append(Spacer(1, 12)) 
                
	        dnm='SAVITRIBAI PHULE PUNE UNIVERSITY'
	        ptext = '<para alignment=\'center\'><html><font size=16>%s</font></html></para>' % dnm
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                im = Image(logo, 1*inch, 1*inch)
                Story.append(im)
	        address_parts = ["Phone:%s"%(email_phone[0][0]),"Email:%s"%(email_phone[0][1])]
	        for part in address_parts:
    		               ptext = '<para alignment=\'right\'><html><font size=12>%s</font></html></para>' % part.strip()
    		               Story.append(Paragraph(ptext, styles["Normal"]))
                               
                               
	        rfn='Ref. No. :  CSD/%s' %rno
                ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%rfn
	        Story.append(Paragraph(ptext, styles["Normal"]))  
	        ptext="<para alignment=\"right\"><html><font size=12>Date:%s</font></html></para>" %dt
                Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                ptext = '<para alignment=\'Center\'><html><font size=12>BONAFIDE CERTIFICATE</font></html></para>' 
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                
       
	        ptext = '<para><html><font size=12>This is to certify that %s %s %s %s(Roll No.%s ) is a regular student of %s,course (year %s) %s at the Department of Computer Science, Savitribai Phule,Pune University.This Certificate has been issued to the student on  %s request for the purpose of %s.As per record of this Department,the other details of the student are as follows:-' %(g,fn,mn,ln,rollno,cource,yy[0],year1,hh,purpose,)
                Story.append(Paragraph(ptext,styles["Normal"])) 
                Story.append(Spacer(1, 30))
                
                ptext = '<html><font size=12>Address:%s</font></html>'%(addl1) 
	        Story.append(Paragraph(ptext, styles["Normal"]))
                ptext = '<font size=12>    %s</font>'%(addl2)
 		
		Story.append(Paragraph(ptext, styles["Normal"])) 
                ptext = '<font size=12>%s</font>'%(addl3)
	        Story.append(Paragraph(ptext, styles["Normal"])) 
          
	        Story.append(Spacer(1, 30))
                ptext = '<font size=12>Date of Birth:%s</font>'%(date)
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(40, 50))   
                
                ptext = '<font size=12>Head</font>'
	        Story.append(Paragraph(ptext, styles["Normal"]))   
    
                doc12.build(Story)
	

                
         if app=='APFS':
   
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
	          
	
	         
         

	         p="""select applicationPurpose from applicationForm where appId='APFS' and rollnumber=%s;"""%(Rollno)
	         cursor.execute(p)
	         val2=cursor.fetchall()
	         purpose= map(lambda x:x[0],val2)[0]
	         
	
	         purpose=''.join(addr_split(purpose))
                 addr=purpose.split(',');
	 	 addr1=','.join(addr[1:]);
        
         	 addr2=''.join(addr_split(addr1))
         
         	 purpose=addr[0]+"\n"+addr2
	         

		 sss4="""select * from applicationProcess.officeContactDetails;"""
    	  	 cursor.execute(sss4)
       	 	 vall4=cursor.fetchall()
         	 email_phone = map(lambda x:x,vall4) 

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
         	 if (cnm[0]=='MCA' or cnm[0]=='mca'):
             		cname='Master of Computer Applications' 
             
         	 else:
             		cname='Master of Computer Science'
		 ss5="""select category from studentDetailsDomain where rollNumber=%s;"""%(Rollno)
    	 	 cursor.execute(ss5)
       	 	 val5=cursor.fetchall()
                 catgry = map(lambda x:x[0],val5) 
                 sss4="""select * from applicationProcess.officeContactDetails;"""
    	 	 cursor.execute(sss4)
       	 	 vall4=cursor.fetchall()
                 y="""select year from courseSemesterDomain where courseId = (select courseId from studentDetailsDomain where rollNumber=%s) and semId = (select semId from studentDetailsDomain where rollNumber=%s);"""
        	 cursor.execute(y,(Rollno,Rollno))
         	 val111=cursor.fetchall()
                 yy= map(lambda x:x[0],val111)
                 if (yy[0]=='1'):
             		yyy='1 st'
         	 elif(yy[0]=='2'):
             		yyy='2 nd'
        	 else:
             		yyy='3 rd'		
                 filename="%s_feestructure.pdf"%(Rollno);
                 
	    	 if val[0][4]=='MCA' or val[0][4]=='mca':  
	           
                   doc12 = SimpleDocTemplate(data.path+"/project_data/doc_pdf/"+filename,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=50,bottomMargin=18)
	           Story=[]
	           magName = "Pythonista"
                   logo = data.path+"/project_data/logo.jpg"
                   im = Image(logo, 1*inch, 1*inch)
                   rno=refn
                   dt=d
                   g=gen
                   msgStr = purpose.replace('\n','<br />')
                   msgStr=msgStr.title()
                   fn =val[0][1].upper()
                   mn =val[0][2].upper()
                   ln =val[0][3].upper()
                   year=yyy
                   cource=cname
                   f1=val[0][6]
                   f2=val[1][6]
	           f3=val[2][6]
	           f4=val[3][6]
	           f5=val[4][6]
	           f6=val[5][6]
	           f7=val[0][7]
	           f8=val[1][7]
	           f9=val[2][7]
	           f10=val[3][7]
	           f11=val[4][7]
	           f12=val[5][7]
                   f13=val[0][8]
	           f14=val[1][8]
	           f15=val[2][8]
	           f16=val[3][8]
	           f17=val[4][8]
	           f18=val[5][8]
	           f19=val[0][9]
	           f20=val[1][9]
	           f21=val[2][9]
	           f22=val[3][9]
                   f23=val[4][9]
                   f24=val[5][9]
	           formatted_time = time.ctime()
	           styles=getSampleStyleSheet()
	           styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	           deptnm='DEPARTMENT OF COMPUTER SCIENCE'
	           ptext = '<para alignment=\'center\'><html><font size=20>%s</font></html></para>' % deptnm
	           Story.append(Paragraph(ptext, styles["Normal"]))
	           Story.append(Spacer(1, 12)) 
                   
	           dnm='SAVITRIBAI PHULE PUNE UNIVERSITY'
	           ptext = '<para alignment=\'center\'><html><font size=16>%s</font></html></para>' % dnm
	           Story.append(Paragraph(ptext, styles["Normal"]))   
	           Story.append(Spacer(1, 12))
                   Story.append(im)
	           address_parts = ["Phone: %s"%(email_phone[0][0]),"Email:%s"%(email_phone[0][2])]
	           for part in address_parts:
    		                  ptext = '<para alignment=\'right\'><html><font size=12>%s</font></html></para>' % part.strip()
    		                  Story.append(Paragraph(ptext, styles["Normal"]))


	           rfn='Ref. No. :  CSD/%s' %rno
	           ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%rfn
	           Story.append(Paragraph(ptext, styles["Normal"]))  
	           ptext="<para alignment=\"right\"><html><font size=12>Date:%s</font></html></para>" %dt
	           Story.append(Paragraph(ptext, styles["Normal"]))   
	           Story.append(Spacer(1, 20))
                   ptext = '<para alignment=\'left\'><html><font size=12>To</font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   ptext = '<para alignment=\'left\'><html><font size=12>The Branch Manager</font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"]))
                   ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%(msgStr)
	           Story.append(Paragraph(ptext, styles["Normal"]))
                   Story.append(Spacer(1, 20))
                   ptext = '<para alignment=\'left\'><html><font size=12>Sir,</font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   
	           ptext = '<para alignment=\'left\'><html>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<font size=12>This letter has been issued on the basis of request by the student for the Purpose of getting Professional Education loan from your Bank.</font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   Story.append(Spacer(1, 10))
                   ptext = '<para alignment=\'left\'><html>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<font size=12>We, hereby certify that %s %s %s %s is a bonafide student of this department studying in %s  year of %s the said course is of 3 year\'s duration.</font></html></para>'%(g,fn,mn,ln,year,cource)
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   Story.append(Spacer(1, 10))
                   ptext = '<para alignment=\'left\'><html><font size=12><u>The minimum fees for Maharashtra Domicile student belonging Open Category are as detailed below. (The tuition & Lab fees may increase as per the university rules & norms)</u> </font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   ptext = '<para alignment=\'center\'><html><font size=12><u>Fees Structure</u></font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"]))  
                   Story.append(Spacer(1, 20))
                   
                   data1 = [["Year ","1st Year ","2nd Year","3nd Year"],
                   ]
                   style = TableStyle([
                                  ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                  ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                   ])
                   
	           #Configure style and word wrap
	           s = getSampleStyleSheet()
	           s = s["BodyText"]
	           s.wordWrap = 'CJK'
	           data11 = [[Paragraph(cell, s) for cell in row] for row in data1]
	           t1=Table(data11)
	           t1.setStyle(style)
                   Story.append(t1)
                   
                   data2 = [["Fees Details","MCA(1st Sem.)","MCA(2nd Sem.)","MCA(3rd Sem.)","MCA(4th Sem.)","MCA(5th Sem.)","MCA(6th Sem.)"],
                            ["Tuition Fees","%s"%(f1),"%s"%(f2),"%s"%(f3),"%s"%(f4),"%s"%(f5),"%s"%(f6)],
                            ["Lab Fees","%s"%(f7),"%s"%(f8),"%s"%(f9),"%s"%(f10),"%s"%(f11),"%s"%(f12)],
                            ["Other Fees","%s"%(f13),"%s"%(f14),"%s"%(f15),"%s"%(f16),"%s"%(f17),"%s"%(f18)],
                            ["Total Fees","%s"%(f19),"%s"%(f20),"%s"%(f21),"%s"%(f22),"%s"%(f23),"%s"%(f24)],
                   ]
                   style = TableStyle([
                                  ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                  ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                   ])
                   
	           #Configure style and word wrap
	           s = getSampleStyleSheet()
	           s = s["BodyText"]
	           s.wordWrap = 'CJK'
	           data22 = [[Paragraph(cell, s) for cell in row] for row in data2]
	           t2=Table(data22)
	           t2.setStyle(style)
                   Story.append(t2)
                   Story.append(Spacer(1, 20))
                   ptext = '<para alignment=\'left\'><html><font size=12><b>The amount towards fees can be paid through the Demand Draft to be in favour of \'Finance & Accounts Officer, Savitribai Phule Pune University\',Payable at Pune.</b> </font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"])) 
                   Story.append(Spacer(40, 50)) 
	           ptext = '<para alignment=\'left\'><html><font size=12>Sincerely Yours,</font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"]))
	           Story.append(Spacer(40, 50)) 
                   ptext = '<para alignment=\'left\'><html><font size=12><b>Head</b></font></html></para>'
	           Story.append(Paragraph(ptext, styles["Normal"]))
	           doc12.build(Story)
                   
                  
                   
	         else:
			


                        doc12= SimpleDocTemplate(data.path+"/project_data/doc_pdf/"+filename,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=50,bottomMargin=18)
	                Story=[]
	                magName = "Pythonista"
                        logo = data.path+"/project_data/logo.jpg"
                        im = Image(logo, 1*inch, 1*inch)
                        rno=refn
                        dt=d
                        g=gen
                        fn = val[0][1].upper()
                        mn = val[0][2].upper()
                        ln = val[0][3].upper()
                        year=yyy
                        msgStr = purpose.replace('\n','<br />')
                        msgStr=msgStr.title()
                        cource=cname
                        f1=val[0][6]
                        f2=val[1][6]
	                f3=val[2][6]
	                f4=val[3][6]
	                f5=val[0][7]
	                f6=val[1][7]
	                f7=val[2][7]
	                f8=val[3][7]
	                f9=val[0][8]
	                f10=val[1][8]
	                f11=val[2][8]
	                f12=val[3][8]
                        f13=val[0][9]
                        f14=val[1][9]
                        f15=val[2][9]
                        f16=val[3][9]
	                formatted_time = time.ctime()
	                styles=getSampleStyleSheet()
	                styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	                deptnm='DEPARTMENT OF COMPUTER SCIENCE'
	                ptext = '<para alignment=\'center\'><html><font size=20>%s</font></html></para>' % deptnm
	                Story.append(Paragraph(ptext, styles["Normal"]))
	                Story.append(Spacer(1, 12)) 
                        
	                dnm='SAVITRIBAI PHULE PUNE UNIVERSITY'
	                ptext = '<para alignment=\'center\'><html><font size=16>%s</font></html></para>' % dnm
	                Story.append(Paragraph(ptext, styles["Normal"]))   
	                Story.append(Spacer(1, 12))
                        Story.append(im)
	                address_parts = ["Phone: %s"%(email_phone[0][0]),"Email:%s"%(email_phone[0][2])]
	                for part in address_parts:
    		                       ptext = '<para alignment=\'right\'><html><font size=12>%s</font></html></para>' % part.strip()
    		                       Story.append(Paragraph(ptext, styles["Normal"]))
                                       
                                       
	                rfn='Ref. No. :  CSD/%s' %rno
	                ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%rfn
	                Story.append(Paragraph(ptext, styles["Normal"]))  
	                ptext="<para alignment=\"right\"><html><font size=12>Date:%s</font></html></para>" %dt
	                Story.append(Paragraph(ptext, styles["Normal"]))   
	                Story.append(Spacer(1, 20))
                        ptext = '<para alignment=\'left\'><html><font size=12>To</font></html></para>'
	           	Story.append(Paragraph(ptext, styles["Normal"])) 
                   	ptext = '<para alignment=\'left\'><html><font size=12>The Branch Manager</font></html></para>'
	           	Story.append(Paragraph(ptext, styles["Normal"]))
                   	ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%(msgStr)
	           	Story.append(Paragraph(ptext, styles["Normal"]))
                        Story.append(Spacer(1, 20))
                        ptext = '<para alignment=\'left\'><html><font size=12>Sir,</font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"])) 
                        
	                ptext = '<para alignment=\'left\'><html>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<font size=12>This letter has been issued on the basis of request by the student for the Purpose of getting Professional Education loan from your Bank.</font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"])) 
                        Story.append(Spacer(1, 10))
                        ptext = '<para alignment=\'left\'><html>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<font size=12>We, hereby certify that %s %s %s %s is a bonafide student of this department studying in %s  year of %s the said course is of 3 year\'s duration.</font></html></para>'%(g,fn,mn,ln,year,cource)
	                Story.append(Paragraph(ptext, styles["Normal"])) 
                        Story.append(Spacer(1, 10))
                        ptext = '<para alignment=\'left\'><html><font size=12><u>The minimum fees for Maharashtra Domicile student belonging Open Category are as detailed below. (The tuition & Lab fees may increase as per the university rules & norms)</u> </font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"])) 
                        ptext = '<para alignment=\'center\'><html><font size=12><u>Fees Structure</u></font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"]))  
                        Story.append(Spacer(1, 20))
                        
                        data1 = [["Year ","1st Year ","2nd Year"],
                        ]
                        style = TableStyle([
                                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                        ])
                        
	                #Configure style and word wrap
	                s = getSampleStyleSheet()
	                s = s["BodyText"]
	                s.wordWrap = 'CJK'
	                data11 = [[Paragraph(cell, s) for cell in row] for row in data1]
	                t1=Table(data11)
	                t1.setStyle(style)
                        Story.append(t1)
                        
                        data2 = [["Fees Details","M.Sc.(1st Sem.)","M.Sc.(2nd Sem.)","M.Sc.(3rd Sem.)","M.Sc.(4th Sem.)"],
                                 ["Tuition Fees","%s"%(f1),"%s"%(f2),"%s"%(f3),"%s"%(f4)],
                                 ["Lab Fees","%s"%(f5),"%s"%(f6),"%s"%(f7),"%s"%(f8)],
                                 ["Other Fees","%s"%(f9),"%s"%(f10),"%s"%(f11),"%s"%(f12)],
                                 ["Total Fees","%s"%(f13),"%s"%(f14),"%s"%(f15),"%s"%(f16)],
                        ]
                        style = TableStyle([
                                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                        ])
                        
	                #Configure style and word wrap
	                s = getSampleStyleSheet()
	                s = s["BodyText"]
	                s.wordWrap = 'CJK'
	                data22 = [[Paragraph(cell, s) for cell in row] for row in data2]
	                t2=Table(data22)
	                t2.setStyle(style)
                        Story.append(t2)
                        Story.append(Spacer(1, 20))
                        ptext = '<para alignment=\'left\'><html><font size=12><b>The amount towards fees can be paid through the Demand Draft to be in favour of \'Finance & Accounts Officer, Savitribai Phule Pune University\',Payable at Pune.</b> </font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"])) 
                        Story.append(Spacer(40, 50)) 
	                ptext = '<para alignment=\'left\'><html><font size=12>Sincerely Yours,</font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"]))
	                Story.append(Spacer(40, 50)) 
                        ptext = '<para alignment=\'left\'><html><font size=12><b>Head</b></font></html></para>'
	                Story.append(Paragraph(ptext, styles["Normal"]))
	                doc12.build(Story)
                        
                    

         if app=="APND":
 
                 
        	ss="""select * from  studentDetailsDomain where rollNumber=%s;;"""%(Rollno)
    	 	cursor.execute(ss)
       	 	val=cursor.fetchall()
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
         	if (cnm[0]=='MCA' or cnm[0]=='mca'):
         	    cname='Master of Computer Applications' 
             
         	else:
         	    cname='Master of Computer Science'

         	sss4="""select * from applicationProcess.officeContactDetails;"""
    	 	cursor.execute(sss4)
       	 	vall4=cursor.fetchall()
         	email_phone = map(lambda x:x,vall4) 
         	

                filename="%s_No_Dues.pdf"%(Rollno)
                doc12 = SimpleDocTemplate(data.path+"/project_data/doc_pdf/"+filename,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=50,bottomMargin=18)

                
                Story=[]
                logo = data.path+"/project_data/logo.jpg"
	        magName = "Pythonista"
                im = Image(logo, 1*inch, 1*inch)
                #Story.append(im)        
                
                
                rno=refn
                dt=d
                g=gen
                nm = val[0][4].upper()+" "+val[0][5].upper()+" "+val[0][5].upper()
                rollno=Rollno
                cource=cname
               
	        formatted_time = time.ctime()
	        styles=getSampleStyleSheet()
	        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	        deptnm='DEPARTMENT OF COMPUTER SCIENCE'
	        ptext = '<para alignment=\'center\'><html><font size=20>%s</font></html></para>' % deptnm
	        Story.append(Paragraph(ptext, styles["Normal"]))
	        Story.append(Spacer(1, 12)) 
                
	        dnm='SAVITRIBAI PHULE PUNE UNIVERSITY'
	        ptext = '<para alignment=\'center\'><html><font size=16>%s</font></html></para>' % dnm
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                im = Image(logo, 1*inch, 1*inch)
                Story.append(im)
	        address_parts = ["Phone: %s"%(email_phone[0][0]),"Email:%s"%(email_phone[0][2])]
	        for part in address_parts:
    		               ptext = '<para alignment=\'right\'><html><font size=12>%s</font></html></para>' % part.strip()
    		               Story.append(Paragraph(ptext, styles["Normal"]))

                Story.append(Spacer(1, 12))
	        rfn='Ref. No. :  CSD/%s' %rno
	        ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%rfn
	        Story.append(Paragraph(ptext, styles["Normal"])) 
                
	        ptext="<para alignment=\"right\"><html><font size=12>Date:%s</font></html></para>" %dt
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 20))
                
               
                to='To'
	        ptext = '<para alignment=\'left\'><html><font size=11>%s</font></html></para>' % to
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                
                
	        ptext = '<para alignment=\'left\'><html><font size=11> 1. Librarian Jaykar Library </font></html></para>'
	        Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11>2. Librarian Computer Science Dept </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"])) 
                ptext = '<para alignment=\'left\'><html><font size=11>3. Hostel Office </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11>4.Refactory</font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11>5.Computer Science Office </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"])) 
	        Story.append(Spacer(1, 12))
                
                ptext = '<para alignment=\'left\'><font size=11>%s %s Roll No.%s.Is leaving the %s (Computer Science) Programs Please recover any dues, outstanding  against %s and give %s no dues.</font>' %(g,nm,rollno,cource,hh,on_print_gender)
                Story.append(Paragraph(ptext,styles["Normal"])) 
	        Story.append(Spacer(40, 50))
               
                ptext = '<para alignment=\'left\'><html><font size=11> Yours  Sincerely. </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                Story.append(Spacer(1, 30))
                ptext = '<para alignment=\'left\'><html><font size=11>.............................................................</font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> Jaykar Library </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
	        Story.append(Spacer(1, 30))
	        ptext = '<para alignment=\'left\'><html><font size=11>.............................................................</font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> Computer Science Library </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
	        Story.append(Spacer(1, 30))
	        ptext = '<para alignment=\'left\'><html><font size=11>.............................................................</font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> Hostel Office  </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
	        Story.append(Spacer(1, 30))
	        ptext = '<para alignment=\'left\'><html><font size=11>.............................................................</font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> Refectory  </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
	        Story.append(Spacer(1, 30))
                
                ptext = '<para alignment=\'left\'><html><font size=11>.............................................................</font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> Computer Science Office </font></html></para>'
                Story.append(Paragraph(ptext,styles["Normal"]))



	        doc12.build(Story)








                
                
         if app=="APIB":

	        doc='';
	                 
	         
		db = MySQLdb.connect(
 	   	host="localhost",
 	   	user=data.mysql_user,
 	   	passwd=data.mysql_pswd,
 	   	db="applicationProcess" )
 	        # prepare a cursor object using cursor() method
 	   	cursor = db.cursor()
 	            
 	         
 	        
 	        
	
 	        
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
                
	        rfno=valu[0][4];
                rpno=valu[0][5];
                unino=valu[0][6];
                svup=valu[0][7]
                rob=valu[0][8]
                exmdt=valu[0][9]
                resldt=valu[0][10]
 	        d=time.strftime("%d/%m/%Y")
                sss4="""select * from applicationProcess.officeContactDetails;"""
    	 	cursor.execute(sss4)
       	 	vall4=cursor.fetchall()
         	email_phone = map(lambda x:x,vall4) 
 	        
 	        
		
                filename="%s_inter_bonafide.pdf"%(Rollno)

                doc12 = SimpleDocTemplate(data.path+"/project_data/doc_pdf/"+filename,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=50,bottomMargin=18)
	        Story=[]
	        magName = "Pythonista"
                logo = data.path+"/project_data/logo.jpg"
                im = Image(logo, 1*inch, 1*inch)
                rno=rfno
                dt=d
                nationality=val1[0][1]
                fn = val[0][4].upper()
                mn = val[0][5].upper()
                ln = val[0][6].upper()
                stud_add_pune=val1[0][2].title()
                contact=val[0][9]
                
                
                pno=val1[0][4]
                vno=val1[0][7]
                issueon=val1[0][5]
                vistype=val1[0][8]
                vissueon=val1[0][9]
                validtill=val1[0][6]
                visavaltill=val1[0][10]
                visaupto=svup;
                date_of_add=val1[0][3]
                cource=val[0][1]
                curr_cource=val[0][1]
                aca_year_month=d
                res=rob
	        formatted_time = time.ctime()
	        styles=getSampleStyleSheet()
	        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	        deptnm='DEPARTMENT OF COMPUTER SCIENCE'
	        ptext = '<para alignment=\'center\'><html><font size=20>%s</font></html></para>' % deptnm
	        Story.append(Paragraph(ptext, styles["Normal"]))
	        Story.append(Spacer(1, 12)) 
                
	        dnm='SAVITRIBAI PHULE PUNE UNIVERSITY'
	        ptext = '<para alignment=\'center\'><html><font size=16>%s</font></html></para>' % dnm
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 12))
                Story.append(im)
	        address_parts = ["Phone:%s"%(email_phone[0][0]),"Email:%s"%(email_phone[0][1])]
	        for part in address_parts:
    		               ptext = '<para alignment=\'right\'><html><font size=12>%s</font></html></para>' % part.strip()
    		               Story.append(Paragraph(ptext, styles["Normal"]))


                rfn='Ref. No. :  CSD/%s' %rno
	        ptext = '<para alignment=\'left\'><html><font size=12>%s</font></html></para>'%rfn
	        Story.append(Paragraph(ptext, styles["Normal"]))  
	        ptext="<para alignment=\"right\"><html><font size=12>Date:%s</font></html></para>" %dt
	        Story.append(Paragraph(ptext, styles["Normal"]))   
	        Story.append(Spacer(1, 20))
                
                ptext = '<para alignment=\'left\'><html><font size=12>This is to certify that %s %s %s is a bonafide student of this department. His particulars as per our record are as follows:</font></html></para>'%(fn,mn,ln)
                Story.append(Paragraph(ptext, styles["Normal"])) 
                Story.append(Spacer(1, 30))
                ptext = '<para alignment=\'left\'><html><font size=11> 1. Name: %s %s %s  </font></html></para>'%(fn,mn,ln)
	        Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 2. Nationality: %s  </font></html></para>'%(nationality) 
                Story.append(Paragraph(ptext,styles["Normal"])) 
                ptext = '<para alignment=\'left\'><html><font size=11> 3. Student\'s Address in Pune: %s </font></html></para>' %(stud_add_pune)
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 4. Contacts: %s </font></html></para>' %(contact)
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 5. R.P. No.:- %s </font></html></para>' %(rpno)
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 6. Unique No.:- %s</font></html></para>' %(unino)
                Story.append(Paragraph(ptext,styles["Normal"]))
                Story.append(Spacer(1, 30))
                data1 = [["Passport details","Visa details"],
                ]
                style = TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black) ])
                
	        #Configure style and word wrap
	        s = getSampleStyleSheet()
	        s = s["BodyText"]
	        s.wordWrap = 'CJK'
	        data11 = [[Paragraph(cell, s) for cell in row] for row in data1]
	        t1=Table(data11)
	        t1.setStyle(style)
                
	        #Send the data and build the file
	        Story.append(t1)
                data2 = [["Passport No.","%s"%(pno),"Visa No.","%s"%(vno)],
                         ["Issued on","%s"%(issueon),"Visa  Type","%s"%(vistype)],
                         ["Valid till","%s"%(validtill),"Issued on","%s"%(vissueon)],
                         ["","","Valid till","%s"%(visavaltill)],
                         ["","","Stay Visa up to","%s"%(visaupto)],
                ]
                style = TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                ])
                
	        #Configure style and word wrap
	        s = getSampleStyleSheet()
	        s = s["BodyText"]
	        s.wordWrap = 'CJK'
	        data22 = [[Paragraph(cell, s) for cell in row] for row in data2]
	        t2=Table(data22)
	        t2.setStyle(style)
                Story.append(t2)
                Story.append(Spacer(1, 30))
                

                ptext = '<para alignment=\'left\'><html><font size=11> 7. Date of  First Admission & Course Name : %s & %s  </font></html></para>'%(date_of_add,cource)
	        Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 8. Current Course & Academic Year With specific month: %s & %s  </font></html></para>'%(curr_cource,aca_year_month) 
                Story.append(Paragraph(ptext,styles["Normal"])) 
                ptext = '<para alignment=\'left\'><html><font size=11> 9. Institute recognized by : Savitribai Phule Pune University.  </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 10. Course recognized by : Savitribai Phule Pune University </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 11. Regular/Backlog student : %s </font></html></para>'%(res)
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 12. Exam Date : %s </font></html></para>' %(str(exmdt))
                Story.append(Paragraph(ptext,styles["Normal"])) 
                ptext = '<para alignment=\'left\'><html><font size=11> 13. Result Date : %s </font></html></para>' %(str(resldt))
                Story.append(Paragraph(ptext,styles["Normal"]))
                ptext = '<para alignment=\'left\'><html><font size=11> 14. Behavior of student :  Satisfactory  </font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"])) 
                ptext = '<para alignment=\'left\'><html><font size=11> 15. Recommended for extension: Yes up to the end of the course.</font></html></para>' 
                Story.append(Paragraph(ptext,styles["Normal"]))
                Story.append(Spacer(60, 80))
                
                ptext = '<para alignment=\'left\'><html><font size=11><b>Date: </b>%s&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b>Official Seal</b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<b>Head</b>  </font></html></para>'%(date_of_add)
	        Story.append(Paragraph(ptext,styles["Normal"]))
                
	        doc12.build(Story)
         fa.append(filename);       
















    for i in fa:
               
    
                     fp=open(data.path+"/project_data/doc_pdf/"+i,"r")
                           
                     zf.write(data.path+"/project_data/doc_pdf/"+i, arcname=i)
    		
    fp1=open(data.path+"/project_data/autoclick8.html")
    fp=fp1.read()   
    return fp
