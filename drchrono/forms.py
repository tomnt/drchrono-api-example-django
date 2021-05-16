from django import forms
from django.forms import widgets


# Add your forms here
from django.contrib.auth import authenticate


class CreateAppointmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)


class AppointmentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AppointmentsForm, self).__init__(*args, **kwargs)
