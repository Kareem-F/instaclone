from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upload_photo/$', views.upload_photo, name='upload_photo'),
    url(r'^update_profile', views.update_profile, name='update_profile'),
    url(r'^search', views.search, name='search'),
    url(r'^(?P<username>[\w\d]+)/$', views.profile, name='profile'),
]
