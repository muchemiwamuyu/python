from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.helloWorld, name='helloWorld'),
    path('blog/', views.Blog_list, name='blog-list'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='edit-blog'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('add_blog/', views.add_blog, name='add-blog'),
]

handler404 = 'authentication.views.error_404'