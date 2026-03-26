
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('/users/')



urlpatterns = [
    path('', home),  # 👈 this is the key line
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]

