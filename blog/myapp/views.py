from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .models import Post


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
