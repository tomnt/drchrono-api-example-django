from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

from drchrono.endpoints import (
    DoctorEndpoint,
    PatientEndpoint,
    AppointmentProfileEndpoint,
    AppointmentEndpoint,
)
import datetime
from .api import Api
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import AppointmentsForm, CreateAppointmentForm
import numpy as np


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """

    template_name = "kiosk_setup.html"


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """

    template_name = "doctor_welcome.html"

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider="drchrono")
        access_token = oauth_provider.extra_data["access_token"]

        # UserSocialAuth.disconnect()

        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs["doctor"] = doctor_details
        return kwargs


statuses = ["", "Confirmed", "In Session", "Complete", "Arrived", "Cancelled"]
colors = {
    "": "",
    "None": "none",
    "Aquamarine": "rgb(108,255,219)",
    "Maya Blue": "rgb(112,216,255)",
    "Columbia Blue": "rgb(144,228,255)",
    "Alice Blue": "rgb(220,229,255)",
    "Rose Bud": "rgb(255,162,148)",
    "Bisque": "rgb(255,222,192)",
    "Blumine": "#1f497d",
    "Limeade": "#4e9a06",
    "Steel Blue": "#4f81bd",
    "Bouquet": "#ad7fa8",
    "Logan": "#b2a2c7",
    "Porsche": "#e9b96e",
    "Corvette": "#fac08f",
}


def appointments_list(request):
    form = AppointmentsForm(request.POST or None)
    doctor_welcome = DoctorWelcome()
    api = Api(doctor_welcome.get_token())
    doctor = doctor_welcome.make_api_request()
    office = api.offices_read({"doctor": doctor["id"]})
    exam_rooms = office["exam_rooms"]
    # Updating schedule
    ####################
    if bool(form.data.get("update")):
        api.appointments_update(
            id=form.data.get("id"),
            data={
                "scheduled_time": form.data.get("s_date")
                + "T"
                + form.data.get("s_time")
                + ":00",
                "duration": form.data.get("duration"),
                "patient": form.data.get("patient"),
                "notes": form.data.get("notes"),
                "reason": form.data.get("reason"),
                "status": form.data.get("status"),
                "exam_room": form.data.get("exam_room"),
                "billing_status": form.data.get("billing_status"),
                "color": form.data.get("color"),
            },
        )
    # Deleting schedule
    ####################
    if bool(form.data.get("delete")):
        api.appointments_update(id=form.data.get("id"), data={"deleted_flag": True})
    # Date range/start & end
    #########################
    if bool(form.data.get("update_range")):
        start = str(form.data.get("start"))
        end = form.data.get("end")
        dt_start = datetime.datetime.strptime(start, "%Y-%m-%d")
        dt_end = datetime.datetime.strptime(end, "%Y-%m-%d")
    else:
        dt_now = datetime.datetime.now()
        dt_start = dt_now + datetime.timedelta(days=-30)
        dt_end = dt_now + datetime.timedelta(days=30)
        start = dt_start.strftime("%Y-%m-%d")
        end = dt_end.strftime("%Y-%m-%d")
    working_days = np.busday_count(dt_start.date(), dt_end.date())
    # Appointments & Patients
    ##########################
    appointments = api.appointments_list(
        start=start, end=end, params={"deleted_flag": False}
    )
    patients = api.patients_list(params={"doctor": doctor["id"]})

    # duration, date & time
    ########################
    duration = 0
    for k, a in enumerate(appointments):
        s = str(a["scheduled_time"]).split("T")
        appointments[k]["s_date"] = s[0]
        appointments[k]["s_time"] = s[1][:-3]
        color = str(a["color"])
        color = color.lower()
        color = color.replace(" ", "")
        appointments[k]["color"] = color
        duration += a["duration"]
    waiting = working_days * 8 * 60 - duration
    # Return
    ##########
    return render(
        request,
        "appointments_list.html",
        {
            "form": form,
            "title": "My Form 123",
            "doctor": doctor,
            "appointments": appointments,
            "patients": patients,
            "exam_rooms": exam_rooms,
            "statuses": statuses,
            "colors": colors,
            "start": start,
            "end": end,
            "waiting": waiting,
            "duration": duration,
        },
    )


def appointments_create(request):
    form = CreateAppointmentForm(request.POST or None)
    doctor_welcome = DoctorWelcome()
    api = Api(doctor_welcome.get_token())
    doctor = doctor_welcome.make_api_request()
    office = api.offices_read({"doctor": doctor["id"]})
    exam_rooms = office["exam_rooms"]
    # api.appointments_create(params = {
    #         "scheduled_time":  form.data.get("s_date")+"T"+form.data.get("s_time")+":00",
    #         "duration":form.data.get("duration"),
    #         "patient": form.data.get("patient"),
    #         "notes": form.data.get("notes"),
    #         "reason": form.data.get("reason"),
    #         "status": form.data.get("status"),
    #         "billing_status": form.data.get("billing_status"),
    #         "color": form.data.get("color"),
    #         "exam_room": "4",
    #         "office": "314046",
    #         })
    patients = api.patients_list(params={"doctor": doctor["id"]})
    # Return
    #########
    return render(
        request,
        "appointments_create.html",
        {
            "form": form,
            "title": "My Form 123",
            "doctor": doctor,
            "patients": patients,
            "exam_rooms": exam_rooms,
            "statuses": statuses,
            "colors": colors,
        },
    )


def patients_list(request):
    form = AppointmentsForm(request.POST or None)
    doctor_welcome = DoctorWelcome()
    api = Api(doctor_welcome.get_token())
    doctor = doctor_welcome.make_api_request()
    office = api.offices_read({"doctor": doctor["id"]})
    exam_rooms = office["exam_rooms"]
    # Updating a patient
    #####################
    if bool(form.data.get("update")):
        data = {
            "chart_id": form.data.get("chart_id"),
            "first_name": form.data.get("first_name"),
            "middle_name": form.data.get("middle_name"),
            "last_name": form.data.get("last_name"),
            "date_of_birth": form.data.get("date_of_birth"),
            "social_security_number": form.data.get("social_security_number"),
            "address": form.data.get("address"),
            "city": form.data.get("city"),
            "state": form.data.get("state"),
            "zip_code": form.data.get("zip_code"),
            "cell_phone": form.data.get("cell_phone"),
            "home_phone": form.data.get("home_phone"),
            "email": form.data.get("email"),
            "date_of_first_appointment": form.data.get("date_of_first_appointment"),
            "date_of_last_appointment": form.data.get("date_of_last_appointment"),
            "gender": form.data.get("gender"),
            "preferred_language": form.data.get("preferred_language"),
            "ethnicity": form.data.get("ethnicity"),
            "race": form.data.get("race"),
            "patient_photo": form.data.get("patient_photo"),
            "primary_care_physician": form.data.get("primary_care_physician"),
            "employer": form.data.get("employer"),
            "employer_address": form.data.get("employer_address"),
            "employer_city": form.data.get("employer_city"),
            "employer_state": form.data.get("employer_state"),
            "employer_zip_code": form.data.get("employer_zip_code"),
            "office_phone": form.data.get("office_phone"),
            "offices": form.data.get("offices"),
            "responsible_party_name": form.data.get("responsible_party_name"),
            "responsible_party_relation": form.data.get("responsible_party_relation"),
            "responsible_party_phone": form.data.get("responsible_party_phone"),
            "responsible_party_email": form.data.get("responsible_party_email"),
            "emergency_contact_name": form.data.get("emergency_contact_name"),
            "emergency_contact_relation": form.data.get("emergency_contact_relation"),
            "emergency_contact_phone": form.data.get("emergency_contact_phone"),
            "disable_sms_messages": form.data.get("disable_sms_messages"),
            "copay": form.data.get("copay"),
        }
        patient_photo_date = form.data.get("patient_photo_date")
        if patient_photo_date:
            data["patient_photo_date"] = patient_photo_date
        api.patients_update(id=form.data.get("id"), data=data)
    # Deleting a patient
    #####################
    if bool(form.data.get("delete")):
        api.appointments_update(id=form.data.get("id"), data={"deleted_flag": True})

    patients = api.patients_list(params={"doctor": doctor["id"]})

    for k, p in enumerate(patients):
        if not p["responsible_party_email"]:
            patients[k]["responsible_party_email"] = ""
        if not p["email"]:
            patients[k]["email"] = ""
        if not p["middle_name"]:
            patients[k]["middle_name"] = ""
        if not p["patient_photo_date"]:
            patients[k]["patient_photo_date"] = ""
        if not p["responsible_party_name"]:
            patients[k]["responsible_party_name"] = ""
        if not p["responsible_party_relation"]:
            patients[k]["responsible_party_relation"] = ""
        if not p["responsible_party_phone"]:
            patients[k]["responsible_party_phone"] = ""
        if not p["emergency_contact_relation"]:
            patients[k]["emergency_contact_relation"] = ""
    return render(
        request,
        "patients_list.html",
        {
            "form": form,
            "title": "My Form 123",
            "doctor": doctor,
            "patients": patients,
            "exam_rooms": exam_rooms,
            "statuses": statuses,
            "colors": colors,
        },
    )
