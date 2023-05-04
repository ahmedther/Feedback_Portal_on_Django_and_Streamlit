from .support_feedback_app import (
    post_request_db_submission,
    get_questions_data,
    send_email_to_department,
    get_patient_details,
)
from .models import SMS_SENT_FOR_FEEDBACK
from django.shortcuts import render


# Create your views here.


def index(request):
    uhid = request.GET.get("uhid")
    encounter_id = request.GET.get("encounter_id")
    if not uhid and not encounter_id:
        return render(request, "feedback_app/index.html")

    patient_details = get_patient_details(uhid, encounter_id)
    if not patient_details:
        context = {
            "error": ["Details not found.", "Check Entered UHID and Encounter ID"]
        }
        return render(request, "feedback_app/index.html", context)

    if request.method == "GET":
        question_info = get_questions_data(patient_details)
        return render(request, "feedback_app/feedback.html", question_info)

    elif request.method == "POST":
        email_dict = post_request_db_submission(request.POST, None, patient_details)
        send_email_to_department(patient_details, email_dict)
        return render(request, "feedback_app/thank_you_page.html")


def feedback(request):
    # Get Mobile Number from the url
    try:
        mob_no = request.GET["mobno"]
    except:
        return render(request, "feedback_app/link_expired.html")
    # Search Patient in the database by the phone number
    try:
        patient_details = SMS_SENT_FOR_FEEDBACK.objects.filter(
            patient_contact_number=mob_no
        ).first()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        # If Patient is not found on the Database Display Expired Link
    if request.method == "GET":
        if not patient_details:
            return render(request, "feedback_app/link_expired.html")

        question_info = get_questions_data(patient_details)

        return render(request, "feedback_app/feedback.html", question_info)

    elif request.method == "POST":
        email_dict = post_request_db_submission(request.POST, mob_no, patient_details)
        send_email_to_department(patient_details, email_dict)

        return render(request, "feedback_app/thank_you_page.html")
