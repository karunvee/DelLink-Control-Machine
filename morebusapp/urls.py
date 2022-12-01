# from django.conf.urls import url
from django.urls import include, path
from . import views
from .views import ErrorStreamView
urlpatterns = [
    # url(r'^$', views.home_view, name='home_view'),
    # url(r'^line_view/ln(?P<ln>[0-9]+)/$', views.line_view, name='line_view'),
    # url(r'^machine_view/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)/$', views.item_view, name='item_view'),
    # url(r'setting/$', views.setting_view, name='setting_view'),
    # url(r'remote/$', views.remote_view, name='remote_view'),
    # url(r'delete_indicator/ln(?P<ln>[0-9]+)id(?P<id>[0-9]+)tag_id(?P<tid>[0-9]+)/$', views.delete_indicator, name='delete_indicator'),
    path('', views.home_view, name='home_view'),
    path('line_view/ln<int:ln>/', views.line_view, name='line_view'),
    path('machine_view/ln<str:ln>id<str:id>/', views.item_view, name='item_view'),
    path('setting/', views.setting_view, name='setting_view'),
    path('notice_view/', views.notice_view, name='notice_view'),
    path('stream_error_msg/', ErrorStreamView.as_view(), name='stream_error_msg'),
    path('camera_view<str:id>/', views.camera_view, name='camera_view'),
    path('delete_indicator/ln<str:ln>id<str:id>tag_id<str:tid>/', views.delete_indicator, name='delete_indicator'),
]