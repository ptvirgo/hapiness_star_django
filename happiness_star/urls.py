from django.conf.urls import url
from . import views

app_name = 'happiness_star'

urlpatterns = [
    url('^$', views.StarFormView.as_view(), name='star_form'),
    url('list/$', views.StarListView.as_view(), name='star_list'),
    url('([\d-]+)/$', views.StarView.as_view(), name='star'),
]
