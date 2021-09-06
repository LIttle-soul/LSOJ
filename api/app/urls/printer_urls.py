from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import printer_views


urlpatterns = [
    url(r'^printer/$', printer_views.PrinterList.as_view()),
    url(r'^printer/(?P<pk>[0-9]+)/$', printer_views.PrinterDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
