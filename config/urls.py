from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('capitals.urls')),
    path('', include('inner_s.user.urls')),
]
