from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q


class MainView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        posts_list = Post.objects.all().order_by('-id')
        paginator = Paginator(posts_list, 6)
        posts = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'myapp/pages/home.html', context={
            'posts': posts,
            'pages': range(1, 4),
        })


class PostDetailView(View):

    @staticmethod
    def get(request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        last_posts = Post.objects.all().order_by('-id')[:5]
        tags = post.tag.split(', ')
        comment_form = CommentForm()
        return render(request, 'myapp/pages/post_detail.html', context={
            'post': post,
            'last_posts': last_posts,
            'tags': tags,
            'tags_count': len(tags),
            'comment_form': comment_form
        })

    @staticmethod
    def post(request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST.get('text')
            username = request.user
            post = get_object_or_404(Post, url=slug)
            comment = Comment.objects.create(
                post=post,
                username=username,
                text=text
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'myapp/pages/post_detail.html', context={
            'comment_form': comment_form
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


class SignInView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'myapp/pages/signin.html', context={
            'form': form
        })

    @staticmethod
    def post(request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('password', Exception('Неверный логин/пароль'))
        return render(request, 'myapp/pages/signin.html', context={
            'form': form
        })


class FeedBackView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myapp/pages/contacts.html', context={
            'form': form,
            'title': 'Напишите нам'
        })

    @staticmethod
    def post(request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            try:
                send_mail(f'От {name} | {subject}', message, email, [
                    'akimow5417@gmail.com'
                ])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('contacts/success')
        return render(request, 'myapp/pages/contacts.html', context={
            'form': form
        })


class SuccessView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'myapp/pages/success.html', context={
            'title': 'Спасибо'
        })


class SearchResultsView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        query = request.GET.get('q')
        page = request.GET.get('page', 1)
        posts = ''
        results = []
        if query:
            results = Post.objects.filter(
                Q(header__icontains=query) | Q(content__icontains=query)
            ).order_by('id')
            paginator = Paginator(results, 3)
            posts = paginator.get_page(page)
        return render(request, 'myapp/pages/search.html', context={
            'title': 'Поиск',
            'posts': posts,
            'count': len(results),
            'pages': range(1, 4),
            'add_params': '&q=' + str(request.GET.get('q'))
        })


class TagView(View):

    @staticmethod
    def get(request, slug, *args, **kwargs):
        posts = Post.objects.filter(tag__iregex=rf'(?<![\w\d]){slug}(?![\w\d])')
        common_tags = Post.get_most_common_tags()
        return render(request, 'myapp/pages/tag.html', context={
            'posts': posts,
            'title': 'Tег: ' + slug,
            'common_tags': common_tags,
        })
