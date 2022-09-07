

# Register your models here.
from django.contrib import admin
from .models import Question,AllDepartment,RefDropdownList,PatientFeedback,SMS_SENT_FOR_FEEDBACK


# Register Models
admin.site.register(Question)
admin.site.register(AllDepartment)
admin.site.register(RefDropdownList)
admin.site.register(PatientFeedback)
admin.site.register(SMS_SENT_FOR_FEEDBACK)




# CHnage admin Panel
admin.site.site_header = "Feedback Portal Admin Panel"
admin.site.site_title = "Feedback Admin Panel"
admin.site.index_title = "Feedback Portal Administration"