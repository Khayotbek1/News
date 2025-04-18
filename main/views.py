from django.shortcuts import render, redirect, get_object_or_404
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

class DetailPageView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        like_articles = Article.objects.filter(category=article.category).order_by('-created_at')[:5]
        context = {
            'article': article,
            'like_articles': like_articles,
        }
        return render(request, 'detail-page.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        Comment.objects.create(
            article=article,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            text=request.POST.get('text'),
        )
        article.comments = Comment.objects.filter(article=article).count()
        article.save()
        return redirect(f'/articles/{slug}/')

