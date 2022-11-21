from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^$', views.home_view, name='home_view'),
    url(r'^line_view/ln(?P<ln>[0-9]+)/$', views.line_view, name='line_view'),
    url(r'^machine_view/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)/$', views.item_view, name='item_view'),
    url(r'setting/$', views.setting_view, name='setting_view'),
]