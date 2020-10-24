"""omazzam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from comments import views
from accounts import views as account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contactus/',include('contactus.urls')),
    path('accounts/signup/', account.signup, name="signup"),
    path('accounts/login/', account.login, name="login"),
    path('accounts/logout/', account.logout, name="logout"),
    path('editeaccount/', account.editeaccount, name="editeaccount"),
    path('accountgetter/', account.accountgetter, name="accountgetter"),
    path('testapi/', account.testapi, name="testapi"),
    #path('accounts/',include('accounts.urls')),
    path('opinionclassifier/',include('opinionclassifier.urls')),
    path('comments/',include('comments.urls')),
    path('commentsclassifier/',include('commentsclassifier.urls')),
]
