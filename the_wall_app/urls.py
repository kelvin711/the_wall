from django.urls import path     
from . import views

urlpatterns = [
    path('', views.register_login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('create_message', views.create_message),
    path('create_comment/<int:message_id>', views.create_comment),
]