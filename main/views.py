from django.shortcuts import render, redirect
from django.views import View
from .models import *

class IndexView(View):
    def get(self, request):
        articles = Article.published_data.order_by('-important', '-views')[:10]
        latest_articles = Article.published_data.order_by('-created_at')[:10]
        most_views_articles = Article.published_data.order_by('-views')[:10]
        moments = Moment.published_data.order_by('-created_at')[:10]
        context = {
            'articles': articles,
            'latest_articles': latest_articles,
            'most_views_articles': most_views_articles,
            'moments': moments,
        }
        return render(request, 'index.html', context)

    def post(self, request):
        newsletter_email = request.POST.get('newsletter_email')
        if newsletter_email is not None:
            NewsLetter.objects.create(email=newsletter_email)
        return redirect('index')
