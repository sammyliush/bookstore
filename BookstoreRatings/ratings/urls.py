from django.urls import path
from ratings import views
from django.contrib import admin

import ratings.views as pview

urlpatterns = [

    path('ratings/', pview.get_rating),
    path('blank/', pview.blank),
    path('ratings', pview.get_rating),
    path('blank', pview.blank)

]