from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tx/<str:pk>/', views.index_description)
]
