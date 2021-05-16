import views
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r"^setup/$", views.SetupView.as_view(), name="setup"),
    url(r"^welcome/$", views.DoctorWelcome.as_view(), name="setup"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"", include("social.apps.django_app.urls", namespace="social")),
    url(r"^appointments_list/$", views.appointments_list, name="appointments_list"),
    url(
        r"^appointments_create/$", views.appointments_create, name="appointments_create"
    ),
    url(r"^patients_list/$", views.patients_list, name="patients_list"),
]
