import psycopg2
import os

from datetime import datetime


db_name = os.environ.get("POSTGRES_DB")
username = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT")


class PostgressDB:
    def __init__(self):
        # Connect to your postgres DB
        self.connection = psycopg2.connect(
            host=host, dbname=db_name, user=username, password=password, port=port
        )
        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()

    def connection_close(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def get_report(self, from_date, to_date):
        get_report_query = f"""
        
                SELECT "patient_uhid" as "UHID", "patient_name" as "PATIENT NAME",
                "patient_gender" as "GENDER","patient_contact_number" AS "MOBILE NUMBER" ,
                "patient_encounter_id" as "ENCOUNTER ID","patient_bed_location" AS "BED lOCATION",
                "patient_bed_number" AS "BED NUMBER","patient_admission_date_time" AS "ADMISSION DATE",
                "patient_discharge_date_time" AS "DISCHARGE DATE","patient_ref" AS "REFERRAL", 
                "comment_in_general" AS "COMMENT ON OVERALL EXPERIENCE", 
                "service_department" as "DEPARTMENT", "question_asked" as "QUESTION", 
                "answer_input" AS "RATING","comment_on_department" as "COMMENT OF DEPARTMENT",
                "feedback_submission_date_time" AS "FEEDBACK SUBMITTED DATE",
                "departments_reply" AS "DEPARTMENTS REPLY", "replier_name" AS "REPLIER NAME",
                "replier_pr_num" AS "REPLIER PR NUMBER", "replier_designation" as "REPLIER DESIGNATION",
                "replied_date" AS "REPLIED DATE"
                FROM  "feedback_app_patientfeedback"
                where "feedback_submission_date_time" BETWEEN date('{from_date}') AND date('{to_date}') + interval '1 day'
                ORDER BY id ASC 

        """

        self.cursor.execute(get_report_query)
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        self.connection_close()
        return data, column_name

    def get_patient_comment(self, uhid, department, encounter_id):
        if encounter_id:
            get_patient_comment = f"""
        
        select patient_name,comment_on_department,patient_encounter_id,feedback_submission_date_time,departments_reply,replier_pr_num,replier_designation from public.feedback_app_patientfeedback
        where patient_uhid = '{uhid}'
        and service_department = '{department}'
		and patient_encounter_id = '{encounter_id}'
        ORDER BY feedback_submission_date_time DESC 
        LIMIT 1

            """
        else:
            get_patient_comment = f"""
        
            select patient_name,comment_on_department,patient_encounter_id,feedback_submission_date_time,departments_reply,replier_pr_num,replier_designation from public.feedback_app_patientfeedback
            where patient_uhid = '{uhid}'
            and service_department = '{department}'
            ORDER BY feedback_submission_date_time DESC 
            LIMIT 1

            """

        self.cursor.execute(get_patient_comment)
        data = self.cursor.fetchall()
        # column_name = [i[0] for i in self.cursor.description]
        self.connection_close()
        return data  # column_name

    def submit_repliers_comments(
        self,
        departments_reply,
        replier_name,
        replier_pr_num,
        replier_designation,
        uhid,
        department,
        encounter_id,
    ):
        todays_day = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        submit_repliers_comments_query = f""" UPDATE public.feedback_app_patientfeedback
                SET departments_reply = '{departments_reply}',
                replied_date = '{todays_day}',
                replier_name= '{replier_name}',
                replier_pr_num = '{replier_pr_num}',
                replier_designation = '{replier_designation}'
                WHERE patient_uhid = '{uhid}'
                and service_department = '{department}'
                and patient_encounter_id = '{encounter_id}'
                """

        self.cursor.execute(submit_repliers_comments_query)
        self.connection.commit()

        self.connection_close()

    # def delete_patient_above_24hr(self):
    #     delete_patient_above_24hr_query = ('''

    #     DELETE FROM "feedback_app_sms_sent_for_feedback"
    #     WHERE "sms_sent_date" < NOW() - INTERVAL '1 DAY'

    #     ''')

    #     self.cursor.execute(delete_patient_above_24hr_query)
    #     self.connection.commit()


if __name__ == "__main__":
    from_date = "2022-07-19"
    db = PostgressDB()
    a = db.get_report(from_date, from_date)
