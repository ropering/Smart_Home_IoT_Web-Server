from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_value', views.get_value),
    path('test', views.test),

]