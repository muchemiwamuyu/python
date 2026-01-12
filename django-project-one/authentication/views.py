from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog, subscriber
from .forms import BlogForm

# Create your views here.

def helloWorld(request):
    return HttpResponse('Hello World')

def Blog_list(request):
    blogs = Blog.objects.all()
    context = { 'blogs': blogs }
    return render(request, 'blog_list.html', context)

# edit the blog
def edit_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return HttpResponse('Blog not found', status=404)

    if request.method == 'POST':
        blog.title = request.POST.get('title', blog.title)
        blog.content = request.POST.get('content', blog.content)
        blog.is_published = 'is_published' in request.POST
        blog.save()
        return redirect('blog-list')

    context = { 'blog': blog }
    return render(request, 'edit_blog.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if subscriber.objects.filter(email=email).exists():
            return HttpResponse('You are already subscribed!')
        else:
            subscriber.objects.create(email=email)
            return redirect('subscribe')
        
    return render(request, 'subscribe.html')

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to create a new Blog object
            blog = form.save(commit=False)  # Use commit=False to modify the object before saving
            blog.save()  # Save the modified Blog object with the author assigned
            
            return redirect('blog-list')  # Redirect to the 'blog_list' view after successful form submission
    else:
        form = BlogForm()
    
    return render(request, 'add_blog.html', {'form': form})

def error_404(request, exception):
    
    return render(request, '404.html')