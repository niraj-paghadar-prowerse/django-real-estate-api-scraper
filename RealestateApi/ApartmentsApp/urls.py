# from django.conf.urls import url
import datetime
from django.urls import include, re_path
from django.urls import register_converter
from ApartmentsApp import views

# from django.conf.urls.static import static

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns=[
    re_path(r'^apartments$',views.apartmentsApi),
    re_path(r'^apartments/date/<yyyy:date>$',views.apartmentsApi),
    re_path(r'^apartment/([0-9]+)$',views.apartmentsApi),
    re_path(r'^apartment/([0-9]+)/date/<yyyy:date>$',views.apartmentsApi),
    re_path(r'^apartment/last$',views.lastApartmentApi),

    re_path(r'^projects$',views.projectsApi),
    re_path(r'^projects/date/<yyyy:date>$',views.projectsApi),
    re_path(r'^project/([0-9]+)/$',views.projectsApi),
    re_path(r'^project/(?P<id>([0-9]+))/(?P<date>\d{4}-\d{2}-\d{2})$',views.projectsApi,),
    re_path(r'^project/last$',views.lastProjectApi),

    re_path(r'^availability$',views.projectAvailabilitiesApi),
    re_path(r'^availability/(?P<id>([0-9]+))$',views.projectAvailabilitiesApi),
    re_path(r'^availability/(?P<id>([0-9]+))/(?P<date>\d{4}-\d{2}-\d{2})$',views.projectAvailabilitiesApi),

    re_path(r'^status$',views.apartmentStatusesApi),
    re_path(r'^status/(?P<id>([0-9]+))$',views.apartmentStatusesApi),
    re_path(r'^status/(?P<id>([0-9]+))/(?P<date>\d{4}-\d{2}-\d{2})$',views.apartmentStatusesApi),

]