from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'$', views.index_view, name='index'),
    url(r'create-post/$', views.create_post_view, name='create-post'),
    url(r'post_detail/(?P<id>[0-9]+)/$', views.post_detail_view,
        name='post-detail'),
    url(r'add-comment/(?P<id>[0-9]+)/$', views.add_comment_view,
        name='add-comment'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
