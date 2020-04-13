from django.urls import path, include
from . import views
urlpatterns = [
    path('contactus/', views.contactus, name="contactus"),
    path('aboutus/', views.aboutus, name="aboutus"),
]
