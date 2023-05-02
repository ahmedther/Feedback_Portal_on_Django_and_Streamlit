from django.db import models

# Create your models here.


class Question(models.Model):

    department = models.CharField(max_length=255)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.department + " - " + self.question


# class Pharmacy(models.Model):
#     department = models.CharField(max_length=255)
#     pharmacy_question = models.CharField(max_length=255)

#     def __str__(self):
#         return self.question


class AllDepartment(models.Model):

    department = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.department


class RefDropdownList(models.Model):

    dropdown_items = models.CharField(max_length=255)

    def __str__(self):
        return self.dropdown_items


class PatientFeedback(models.Model):
    patient_uhid = models.CharField(max_length=255, null=True)
    patient_name = models.CharField(max_length=255, null=True)
    patient_encounter_id = models.CharField(max_length=255, null=True)
    patient_contact_number = models.CharField(max_length=255, null=True)
    patient_gender = models.CharField(max_length=255, null=True)
    patient_bed_number = models.CharField(max_length=255, null=True)
    patient_bed_location = models.CharField(max_length=255, null=True)
    patient_admission_date_time = models.DateTimeField(null=True)
    patient_discharge_date_time = models.DateTimeField(null=True)
    service_department = models.CharField(max_length=255, null=True)
    question_asked = models.CharField(max_length=255, null=True)
    question_code = models.CharField(max_length=255, null=True)
    answer_input = models.CharField(max_length=255, null=True)
    comment_on_department = models.TextField(max_length=524288, null=True)
    comment_in_general = models.TextField(max_length=524288, null=True)
    patient_ref = models.CharField(max_length=255, null=True)
    feedback_submission_date_time = models.DateTimeField(null=False)
    departments_reply = models.TextField(max_length=524288, null=True)
    replier_name = models.CharField(max_length=255, null=True)
    replier_designation = models.CharField(max_length=255, null=True)
    replier_pr_num = models.CharField(max_length=255, null=True)
    replied_date = models.DateTimeField(null=True)

    def __str__(self):

        return self.patient_uhid + " - " + self.patient_name
        # return str(self.patient_uhid) + " - " + self.question_code
        #  def __str__(self):
        # self.feedback_submission_date_time_pf.strftime("dd-mm-yyyy")
        # return self.patient_name + " - " + self.patient_uhid + " "
        # return self.patient_name
        # + " " + self.patient
        # + " " + day
        # return self.service_department


class SMS_SENT_FOR_FEEDBACK(models.Model):
    patient_uhid = models.CharField(max_length=255, null=True)
    encounter_id = models.CharField(max_length=255, null=True)
    patient_name = models.CharField(max_length=255, null=True)
    patient_contact_number = models.CharField(max_length=255, null=True)
    patient_gender = models.CharField(max_length=255, null=True)
    patient_bed_number = models.CharField(max_length=255, null=True)
    patient_bed_location = models.CharField(max_length=255, null=True)
    patient_admission_date_time = models.DateTimeField(null=True)
    patient_discharge_date_time = models.DateTimeField(null=True)
    sms_sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.patient_name + " - " + self.patient_uhid
