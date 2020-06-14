from django.urls import path, re_path, include
from billApp import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table_detail'),
    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(),
            name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(),
            name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(),
            name='lignefacture_update'),
    re_path(r'^facture_update/(?P<pk>\d+)/$', views.FactureUpdate.as_view(), name='facture_detail'),

    # urls for client
    path('client_table_detail/', views.ClientDetailView.as_view(), name='client_table_detail'),
    path('fournisseur_table_detail/', views.FournisseurDetailView.as_view(), name='fournisseur_table_detail'),
    re_path(r'^client_table_create/$', views.ClientCreateView.as_view(),
            name='client_table_create'),
    re_path(r'^fournisseur_table_create/$', views.FournisseurCreateView.as_view(),
            name='fournisseur_table_create'),
    re_path(r'^facture_create/(?P<client_pk>\d+)/$', views.FactureCreateView.as_view(),
            name='facture_create'),
    re_path(r'^client_facture_list/(?P<pk>\d+)/$', views.ClientFactureList.as_view(),
            name='client_facture_list'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(),
            name='client_delete'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),
            name='client_update'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(),
            name='fournisseur_delete'),
    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(),
            name='fournisseur_update'),

    path("dashboard/", views.Dashboard, name="dashboard")
]
