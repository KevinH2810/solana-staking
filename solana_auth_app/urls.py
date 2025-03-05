from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('request-challenge/', views.request_challenge, name='request_challenge'),
    path('verify-signature/', views.verify_signature, name='verify_signature'),
    path('logout/', views.logout_view, name='logout'),
]
