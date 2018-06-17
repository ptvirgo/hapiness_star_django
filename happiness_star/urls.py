from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'happiness_star'

urlpatterns = [
    url('^$', views.StarFormView.as_view(), name='star_form'),
    url('list/$', views.StarListView.as_view(), name='star_list'),
    url('([\d-]+)/$', views.StarView.as_view(), name='star'),
    url('elm/', TemplateView.as_view(template_name='happiness_star/elm.html'))
]
