from .support_feedback_app import (
    post_request_db_submission,
    get_method_data,
    send_email_to_department,
)
from .models import SMS_SENT_FOR_FEEDBACK
from django.shortcuts import render


# Create your views here.


def index(request):

    return render(request, "feedback_app/index.html")


def feedback(request):

    if request.method == "GET":
        # Get Mobile Number from the url
        global mob_no
        try:
            mob_no = request.GET["mobno"]
        except:
            return render(request, "feedback_app/link_expired.html")
        # Search Patient in the database by the phone number
        global patient_details
        try:
            patient_details = SMS_SENT_FOR_FEEDBACK.objects.filter(
                patient_contact_number=mob_no
            ).first()

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        # If Patient is not found on the Database Display Expired Link Page
        if not patient_details:
            return render(request, "feedback_app/link_expired.html")

        question_info = get_method_data(patient_details)

        return render(request, "feedback_app/feedback.html", question_info)

    elif request.method == "POST":

        request_post = request.POST
        post_request_db_submission(request_post, mob_no, patient_details)
        send_email_to_department(patient_details)

        return render(request, "feedback_app/thank_you_page.html")
