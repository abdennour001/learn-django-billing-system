from django.urls import path, re_path, include
from billApp import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail')
]