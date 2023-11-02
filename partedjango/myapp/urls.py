from django.urls import path
from . import views

urlpatterns = [
    path('myform/', views.myform_view, name='myform'),
    path('get_response/', views.obtenerMensajes, name='get_response'),
    path('get_response2/', views.obtenerConfiguracion, name='get_response2'),
    path('get_response3/', views.obtenerConfiguracion, name='get_response3'),
    path('get_response4/', views.ayuda, name='get_response4')
]