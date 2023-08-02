from django.shortcuts import render
from django.http import HttpResponse
from .models import BlogPost


# Create your views here.
def index(request):
    blogs = BlogPost.objects.all()
    params = {'blogs': blogs}
    return render(request, 'blog/index.html', params)


def blogpost(request, id):
    blog = BlogPost.objects.filter(blog_id=id)
    params = {'blog': blog[0]}
    return render(request, 'blog/blogpost.html', params)
