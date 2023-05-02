from django.utils.text import slugify
from datetime import datetime

from .models import (
    PatientFeedback,
    SMS_SENT_FOR_FEEDBACK,
    Question,
    AllDepartment,
    RefDropdownList,
)
from feedback_app.email_sender import Email_Sender
from feedback_app.oracle_config import Ora
from feedback_app.patients_class import Patients


def get_questions_data(patient_details):
    # Declare Global so that we can use all this vaiables in the post request
    departments = AllDepartment.objects.values().order_by("id")
    questions = Question.objects.values().order_by("id")
    dropdown_items = RefDropdownList.objects.all()

    question_info = {
        "departments": departments,
        "questions": questions,
        "dropdown_items": dropdown_items,
        "patient_details": patient_details,
    }

    return question_info


def get_patient_details(uhid, encounter_id):
    db = Ora()
    [patient_data] = db.get_discharge_patients(uhid, encounter_id)
    # Filter M to Male and F to Female
    try:
        if patient_data[4] == "M":
            gender = "Male"

        if patient_data[4] == "F":
            gender = "Female"
    except:
        pass

    patient_details = Patients(
        uhid=patient_data[0],
        encounter_id=patient_data[1],
        name=patient_data[2],
        contact_number=patient_data[3],
        gender=gender,
        bed_number=patient_data[5],
        bed_location=patient_data[6],
        admission_date_time=patient_data[7],
        discharge_date_time=patient_data[8],
    )
    return patient_details


def post_request_db_submission(request_post, mob_no, patient_details):
    # Making global dictionary to send email later
    email_dict = {}
    departments = AllDepartment.objects.values().order_by("id")
    questions = Question.objects.values().order_by("id")
    # Skip Saving CRSF Token to the database
    # iterate through all the data from user input
    for post in request_post:
        if post == "csrfmiddlewaretoken":
            pass
        else:
            patient_info = PatientFeedback()
            # identifying department to save
            for department in departments:
                slug_department = slugify(department["department"])
                #     #print(len(slug_department))
                if slug_department in post:
                    patient_info.service_department = department["department"]
                    patient_info.comment_on_department = request_post[
                        f"patient comment on {patient_info.service_department}"
                    ]
                    email_dict[department["department"]] = (
                        request_post[
                            f"patient comment on {patient_info.service_department}"
                        ],
                        department["email_id"],
                    )

            # identifying Question to save
            for question in questions:
                if post == slugify(question["department"] + "-" + question["question"]):
                    patient_info.question_asked = question["question"]
                    patient_info.question_code = post
                    patient_info.answer_input = request_post[post]
                    # Saving Patient Information to the database
                    # patient_info.comment_in_general = request_post["patient comment"]
                    patient_info.patient_ref = request_post["patient_ref_by"]
                    patient_info.comment_in_general = request_post["patient comment"]
                    patient_info.patient_uhid = patient_details.patient_uhid
                    patient_info.patient_name = patient_details.patient_name
                    patient_info.patient_encounter_id = patient_details.encounter_id
                    patient_info.patient_contact_number = (
                        patient_details.patient_contact_number
                    )
                    patient_info.patient_gender = patient_details.patient_gender
                    patient_info.patient_bed_number = patient_details.patient_bed_number
                    patient_info.patient_bed_location = (
                        patient_details.patient_bed_location
                    )
                    patient_info.patient_admission_date_time = (
                        patient_details.patient_admission_date_time
                    )
                    patient_info.patient_discharge_date_time = (
                        patient_details.patient_discharge_date_time
                    )
                    patient_info.feedback_submission_date_time = (
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    patient_info.save()

            # Delete Patient Record from Sent SMS Table.
            if mob_no:
                try:
                    remove_patient = SMS_SENT_FOR_FEEDBACK.objects.filter(
                        patient_contact_number=mob_no
                    )
                    remove_patient.delete()
                except:
                    pass
    return email_dict


def send_email_to_department(patient_details, email_dict):
    for dep in email_dict:
        Email_Sender(
            # Can write any email id of the organizations
            "FeedBack Report Comment <no.reply@kokilabenhospitals.com>",
            # This is Department's Email iD and "To" in Email Sender Parameter
            email_dict[dep][1],
            # Can write any email id of the organizations
            "no_reply@kokilabenhospitals.com",
            # Subject
            f"{patient_details.patient_name} - {patient_details.patient_uhid}  -  {patient_details.patient_contact_number}",
            f"--- The Following Message is from Patient {patient_details.patient_name} ---\n\n\n\n{email_dict[dep][0]}\n\n\n\n ",
            "172.20.200.29",
            25,
        )
