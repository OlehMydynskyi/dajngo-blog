from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    #Home page
    path('', views.index, name='index'),

    #Display list of blogs
    path('blogs/', views.blogs_page, name='blogs_page'),

    #Display all posts of the blog
    path('posts/<int:blog_id>/', views.posts_page, name='post_page'),

    #Add a new blog
    path('new_blog/', views.new_blog, name='new_blog'),

    #Edit the post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

    #Add a new post
    path('new_post/<int:blog_id>/', views.new_post, name='new_post'),
]
