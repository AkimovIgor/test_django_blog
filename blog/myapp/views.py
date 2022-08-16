from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Post
from .forms import SignUpForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect


class MainView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        posts_list = Post.objects.all().order_by('-id')
        paginator = Paginator(posts_list, 6)
        posts = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'myapp/pages/home.html', context={
            'posts': posts,
            'pages': range(1, 4)
        })


class PostDetailView(View):

    @staticmethod
    def get(request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        last_posts = Post.objects.all().order_by('id')[:5]
        tags = post.tag.split(', ')
        return render(request, 'myapp/pages/post_detail.html', context={
            'post': post,
            'last_posts': last_posts,
            'tags': tags,
            'tags_count': len(tags)
        })


class SignUpView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'myapp/pages/signup.html', context={
            'form': form
        })

    @staticmethod
    def post(request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myapp/pages/signup.html', context={
            'form': form
        })
