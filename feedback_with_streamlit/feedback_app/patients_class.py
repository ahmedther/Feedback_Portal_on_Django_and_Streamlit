class Patients:
    def __init__(
        self,
        uhid,
        encounter_id,
        name,
        contact_number,
        gender,
        bed_number,
        bed_location,
        admission_date_time,
        discharge_date_time,
    ):
        self.patient_uhid = uhid
        self.encounter_id = encounter_id
        self.patient_name = name
        self.patient_contact_number = contact_number
        self.patient_gender = gender
        self.patient_bed_number = bed_number
        self.patient_bed_location = bed_location
        self.patient_admission_date_time = admission_date_time
        self.patient_discharge_date_time = discharge_date_time
