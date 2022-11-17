"""project_space URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from morebusapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home_view, name='home_view'),
    url(r'^line_view/ln(?P<ln>[0-9]+)/$', views.line_view, name='line_view'),
    url(r'^machine_view/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)/$', views.item_view, name='item_view'),
    # url(r'^machine_view/id(?P<id>[0-9]+)/writeData/tag(?P<tg>[0-9]+)/$', views.writeData, name='writeData'),
    url(r'setting/$', views.setting_view, name='setting_view'),
]
