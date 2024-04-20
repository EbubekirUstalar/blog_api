from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('success_load/', views.success_load),
    path('fail_load/', views.fail_load),
    path('list/', views.list),
    path('delete/', views.delete),
]
