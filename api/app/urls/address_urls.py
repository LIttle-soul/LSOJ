from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import address_views


urlpatterns = [
    url(r'^province/$', address_views.ProvinceList.as_view()),
    url(r'^province/(?P<pk>[0-9]+)/$', address_views.ProvinceDetail.as_view()),
    url(r'^municipality/$', address_views.MunicipalityList.as_view()),
    url(r'^municipality/(?P<pk>[0-9]+)/$', address_views.MunicipalityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
