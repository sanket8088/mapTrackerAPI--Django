from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.add),
    path('search/', views.search),
]
