from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0, "Draft"),
    (1, "Published")
)


class Author(models.Model):
    name = models.TextField(max_length=255)
    bio = models.TextField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', max_length=255, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, default=0)
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    rating = models.CharField(max_length=200, default=0)
    users_rated = models.CharField(max_length=200, default=0)
    brand = models.CharField(max_length=250, default=0)
    asin = models.CharField(max_length=250, unique=True)
    tag = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name
