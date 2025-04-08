# netbox/plugins/module_inventory_binder/urls.py

from django.urls import path
from . import views

app_name = 'module_swap'  # Musí odpovídat názvu pluginu

urlpatterns = [
    path('step1/', views.Step1SelectView.as_view(), name='step1_select'),
    path('step2/', views.Step2BayView.as_view(), name='step2_bay'),
]
