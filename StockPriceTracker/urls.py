from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks/', views.stocks, name='stocks'),
    path('info/', views.info, name='info'),
    path('update/', views.update, name='update')
]