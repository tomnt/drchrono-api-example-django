from django import forms
from django.forms import widgets


# Add your forms here
# Added
from django.contrib.auth import authenticate

# from django import forms


class CreateAppointmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)


class AppointmentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
