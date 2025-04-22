from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Count
from django.http import HttpResponse
from .models import *

class IndexView(View):
    def get(self, request):
        articles = Article.published_data.order_by('-important', '-views')[:10]
        latest_articles = Article.published_data.order_by('-created_at')[:10]
        most_views_articles = Article.published_data.order_by('-views')[:10]
        moments = Moment.published_data.order_by('-created_at')[:10]
        categories = Category.objects.annotate(article_count=Count('article')).order_by('-article_count').distinct()
        context = {
            'articles': articles,
            'latest_articles': latest_articles,
            'most_views_articles': most_views_articles,
            'moments': moments,
            'categories': categories,
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
    


class ContactUsView(View):
    def get(self, request):
        return render(request, 'contact.html')
    
    def post(self, request):
        Contact.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone_number = request.POST.get('phone_number'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )

        return HttpResponse("Ma'lumotlaringiz yuborildi! <a href='/'> Bosh sahifa</a>")
    

def newsletter_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        NewsLetter.objects.create(
            email = email
        )
    return redirect('index')


class CategoryArticlesView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        articles = Article.published_data.filter(category=category).order_by('-created_at')
        context = {
            'category': category,
            'articles': articles,
        }
        return render(request, 'category_articles.html', context)




 