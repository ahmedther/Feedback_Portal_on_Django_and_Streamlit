import cx_Oracle as oracle

#from oracle_config import *

ip = "172.20.100.121"

host = "emdb1-vip.kdahit.com"

port = 1521

service_name =  "EMRAC.kdahit.com"

instance_name = "EMRAC1"



#ora_db = oracle.connect("appluser","appluser",dsn_tns)

#cursor = ora_db.cursor()


# host = 'khdb-scan'

# port = 1521

# service_name = "newdb.kdahit.com"

# instance_name = "NEWDB"

# dsn_tns = oracle.makedsn(ip,port,instance_name)

# ora_db = oracle.connect("ibaehis","ib123",dsn_tns)

# cursor = ora_db.cursor()



    #   'oracle': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': 'NEWDB:1521/newdb.kdahit.com',
    #     'NAME': ('(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=khdb-scan)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=newdb.kdahit.com)))'),
    #     'USER': 'ibaehis',
    #     'PASSWORD': 'ib123',


class Ora:

    def __init__(self):
        self.dsn_tns = oracle.makedsn(ip,port,instance_name)
        self.ora_db = oracle.connect("ibaehis","ib123",self.dsn_tns)
        self.cursor = self.ora_db.cursor()

    def status_update(self):

        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department" 

     


    #def __del__(self):
        #self.cursor.close()
        #self.ora_db.close()
    

    def get_patient_details(self,mob_no):

        dpatient_details_qurey = ('''
        
        
            select distinct PATIENT_ID,PATIENT_NAME,CONTACT_NO,gender,BED_NUM,LONG_DESC,ADMISSION_DATE_TIME,DIS_ADV_DATE_TIME 
            from predischarge_feedback_sms
            where CONTACT_NO = :mob_no

        ''')

        self.cursor.execute(dpatient_details_qurey,[mob_no])
        
        patient_details = self.cursor.fetchall()
                 
        return patient_details
    




    def close_database_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()
            


    

if __name__ == "__main__":
    a = Ora()
    #b = a.get_online_consultation_report('01-Mar-2022','03-Apr-2022')
    b = a.get_package_contract_report('16-Jun-2018','12-Jan-2022','KH')

    print(b)

    for x in b:
        print(x)