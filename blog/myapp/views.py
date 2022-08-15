from django.shortcuts import render
from django.views import View


class MainView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'myapp/index.html')
