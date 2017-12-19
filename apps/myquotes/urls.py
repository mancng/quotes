from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_user', views.register_user),
    url(r'^login_user', views.login_user),
    url(r'^logout', views.logout),
    url(r'^quotes', views.quotes),
    url(r'^users/(?P<user_id>\d+)$', views.user),
    url(r'^add_quote', views.add_quote),
    url(r'^add_fav/(?P<quote_id>\d+)$', views.add_fav),
    url(r'^remove_fav/(?P<quote_id>\d+)$', views.remove_fav),

]
