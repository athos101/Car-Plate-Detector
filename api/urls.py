from django.urls import path
from .views import PlateOCRView

urlpatterns = [
    path('read-plate/', PlateOCRView.as_view(), name='read-plate'),
]