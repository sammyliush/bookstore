from django.urls import path
from reviews import views
from django.contrib import admin

import reviews.views as pview

urlpatterns = [

    path('reviews/', pview.get_review),
    path('blank/', pview.blank),
    path('reviews', pview.get_review),
    path('blank', pview.blank)

]