"""CRMDemo URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from app03 import views as view2

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^test/$', views.test),
    url(r'^fotest/$', view2.fotest),
    url(r'^student_login/$', views.student_login),
    url(r'^subscrib/$', view2.subscrib),
    url(r'^getmeeting/$', view2.getmeeting),
    url(r'^subscrib2/$', view2.subscrib2),
    url(r'^answering/(?P<clsid>\d+)/(?P<qsnreid>\d+)/$', views.answering),
    url(r'^questionnairemanage/$', views.questionnairemanage),
    url(r'^questionnairemanage/add/$', views.questionnaireadd),
    url(r'^questionnaire/edit/(?P<clsid>\d+)/(?P<qsnreid>\d+)/$', views.questionnaireedit),
    url(r'^questionnaire2/edit/(?P<clsid>\d+)/(?P<qsnreid>\d+)/$', views.questionnaireedit2),
]
