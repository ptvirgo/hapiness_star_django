from django.conf.urls import url
from . import views

app_name = 'happiness_star'

urlpatterns = [
    url(r'^$', views.StarFormView.as_view(), name='star_form'),
    url(r'^([\d-]+)/$', views.StarView.as_view(), name='star'),
    url(r'^list/$', views.StarListView.as_view(), name='star_list'),
]
