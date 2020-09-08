from django.urls import path, include
from . import views
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('editeaccount/', views.editeaccount, name="editeaccount"),
    path('accountgetter/', views.accountgetter, name="accountgetter"),
    path('testapi/', views.testapi, name="testapi"),

]
