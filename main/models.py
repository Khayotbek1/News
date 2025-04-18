from django.db import models
from django.utils.text import slugify
from .managers import *

class Category(models.Model):
      name = models.CharField(max_length=255)

      def __str__(self):
          return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    intro = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='article/', blank=True, null=True)
    read_time = models.DurationField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    comments = models.SmallIntegerField(default=0)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()
    published_data = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.important:
            Article.objects.exclude(id = self.pk).filter(important=True).update(important=False)

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Contex(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='article-contex', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.article}: {self.text}"

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.CharField(max_length=500)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Moment(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='moment/')
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    objects = models.Manager()
    published_data = PublishedManager()

    def __str__(self):
        return self.title



