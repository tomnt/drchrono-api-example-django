from django import forms
from django.forms import widgets


# Add your forms here
# Added
from django.contrib.auth import authenticate
#from django import forms

class CreateAppointmentForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(CreateAppointmentForm, self).__init__(*args, **kwargs)

class MyForm(forms.Form):
	# username = forms.CharField()
	# password = forms.CharField(widget = forms.PasswordInput,)
	def __init__(self, *args, **kwargs):
		super(MyForm, self).__init__(*args, **kwargs)
		# self.fields['username'].widget.attrs.update({
		#     'class': 'form-control',
		#     "name":"username"})
		# self.fields['password'].widget.attrs.update({
		#     'class': 'form-control',
		#     "name":"password"})
