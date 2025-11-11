from django.contrib import admin
from django.urls import include, path

from api.views import upload_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', upload_page, name='upload-page'), 
]

