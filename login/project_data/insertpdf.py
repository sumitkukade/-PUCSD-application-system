import MySQLdb
import time;
#sfrom mysql.connector import MySQLConnection, Error
#from python_mysql_dbconfig import read_db_config

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo
 
def update_blob(fid, filename):

         # read file
    data = read_file(filename)
 
    # prepare update query and data
    query = """ insert into pdf values(%s,%s);"""
 
    args = (data, fid)
 
    #db_config = read_db_config()
 
    db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="pranali",
    db="mysql" )
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    




def main():
    update_blob(144, "/home/pranali/Downloads/16101_FEES_STRUCTURE.pdf")
 
if __name__ == '__main__':
    main()
