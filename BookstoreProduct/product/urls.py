from django.urls import path
from product import views
from django.contrib import admin

import product.views as pview

urlpatterns = [

    path('blank', pview.blank),
    path('details', pview.details),
    path('ratings', pview.ratings),
    path('blank/', pview.blank),
    path('details/', pview.details),
    path('ratings/', pview.ratings),
    path('', pview.product),
    path('/', pview.product)

]