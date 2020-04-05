from django.urls import path
from details import views
from django.contrib import admin

import details.views as pview

urlpatterns = [

    path('details/', pview.get_detail),
    path('blank/', pview.blank),
    path('details', pview.get_detail),
    path('blank', pview.blank)

]