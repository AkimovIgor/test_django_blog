from django.shortcuts import render
from django.views import View
from .models import Post


class MainView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, 'myapp/pages/home.html', context={
            'posts': posts
        })
