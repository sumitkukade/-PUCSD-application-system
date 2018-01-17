from passlib.apache import HtpasswdFile

name = ""
pwd = ""
ht = HtpasswdFile(".staff.htpasswd")
ht.set_password(name, pwd)
ht.save()
