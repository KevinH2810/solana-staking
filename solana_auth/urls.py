from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login),
    path('admin/', admin.site.urls),
    path('auth/', include('solana_auth_app.urls')),
]
