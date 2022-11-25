from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    # url(r'^$', views.home_view, name='home_view'),
    # url(r'^line_view/ln(?P<ln>[0-9]+)/$', views.line_view, name='line_view'),
    # url(r'^machine_view/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)/$', views.item_view, name='item_view'),
    # url(r'setting/$', views.setting_view, name='setting_view'),
    # url(r'remote/$', views.remote_view, name='remote_view'),
    # url(r'delete_indicator/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)tag_id(?P<tid>[0-9]+)/$', views.delete_indicator, name='delete_indicator'),
    path('', views.home_view, name='home_view'),
    path('line_view/ln<int:ln>/', views.line_view, name='line_view'),
    path('machine_view/ln<int:ln>id<int:id>/', views.item_view, name='item_view'),
    path('setting/', views.setting_view, name='setting_view'),
    path('remote/', views.remote_view, name='remote_view'),
    path('delete_indicator/ln<int:ln>id<int:id>tag_id<int:tid>/', views.delete_indicator, name='delete_indicator'),
]