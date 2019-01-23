"""socialnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from socialnetworkapp.views import *

urlpatterns = [
	url(r'^users/', UserList.as_view(), name='user-list'),
    url(r'^post/(?P<pk>.+)/', PostDetail.as_view(), name='post-one'),
	url(r'^posts', PostList.as_view(), name='post-list'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token/login/', obtain_jwt_token),
    url(r'^token/refresh/', refresh_jwt_token),
    url(r'^token/verify/', verify_jwt_token),    

    url(r'^', include((urlpatterns, 'socialnetworkapp'), namespace='socialnetworkapp'))
]
