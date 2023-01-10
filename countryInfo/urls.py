from django.urls import path
from .views import CountryInfoView

urlpatterns = [
    path('country_info/<str:country_name>/', CountryInfoView.as_view(), name="country_info"),
]