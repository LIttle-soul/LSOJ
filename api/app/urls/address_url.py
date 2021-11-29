from django.urls import path
from app.view.address_view import *

urlpatterns = [
    path('synchronizeaddress/', SynchronizeAddress.as_view(), name='SynchronizeAddress'),
    path('getprovince/', GetProvince.as_view(), name='GetProvince'),
    path('getmunicipality/', GetMunicipality.as_view(), name='GetMunicipality'),
    path('getaddresslist/', GetAddressList.as_view(), name='GetAddressList'),
    path('getaddressmessage/', GetAddressMessage.as_view(), name='getAddressMessage'),
]
