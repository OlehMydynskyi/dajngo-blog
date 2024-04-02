from django.shortcuts import render, redirect
from .models import Blog, Post
from .form import BlogForm, PostForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def check_owner(blog, request):
    if blog.owner != request.user:
        raise Http404

def index(request):
    return render(request, 'index.html')

@login_required
def blogs_page(request):
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    content = {'blogs': blogs}
    return render(request, 'blogs_page.html', content)

@login_required
def posts_page(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    check_owner(blog, request)
    posts = blog.post_set.order_by('-date_added')
    content = {'blog': blog, 'posts': posts}
    return render(request, 'posts_page.html', content)

@login_required
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid:
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs_page')

    context = {'form': form}
    return render(request, 'new_blog.html', context)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    blog = post.blog
    check_owner(blog, request)
    print("-" * 50)
    print(PostForm())
    print("-" * 50)
    test = PostForm(instance=blog)
    print(test)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('blogs:post_page', blog_id=blog.id)

    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'edit_post.html', context)

@login_required
def new_post(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    check_owner(blog, request)

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)

        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:post_page', blog_id=blog_id)
        
    context = {'form': form, 'blog': blog}
    return render(request, 'new_post.html', context)
