from django.shortcuts import render
from django.views import View
from .models import *

class IndexView(View):
    def get(self, request):
        articles = Article.objects.order_by('-important', '-views')[:10]
        context = {
            'articles': articles
        }
        return render(request, 'index.html', context)
