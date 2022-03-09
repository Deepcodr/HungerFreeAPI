from django.urls import path,include,re_path
from hAPI import views
from django.conf.urls.static import static

urlpatterns=[
    path('request/',views.requests),
    path('donation/',views.donations),
    path('userdata/',views.getuserdata)
]