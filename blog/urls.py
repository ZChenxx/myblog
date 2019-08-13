from django.urls import path,re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.ArticleListView.as_view(),name='article_list'),
    re_path(r'^article/create/$',views.ArticleCreateView.as_view(), name='article_create'),
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/$',views.ArticleDetailView.as_view(),name='article_detail'),
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/update/$',views.ArticleUpdateView.as_view(),name='article_update'),
    re_path(r'^tag/add/$',views.TagsCreateView.as_view(),name='tag_add'),
]