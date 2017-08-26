from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^main/$', views.index),
    url(r'^create$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard/$', views.dashboard),
    url(r'^items/add$',views.add_item_get),
    url(r'^items/newitem/$', views.add_item_post),
    url(r'^items/(?P<id>\d+)$', views.view_item),
    url(r'^items/delete/(?P<id>\d+)$', views.delete_item),
    url(r'^items/wishlist/add/(?P<id>\d+)$', views.add_item_wishlist),
    url(r'^items/wishlist/delete/(?P<id>\d+)$', views.delete_item_wishlist),
]
