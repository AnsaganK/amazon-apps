from django.shortcuts import render
from django.views import generic
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            prev_article = Post.objects.get(id=self.object.id-1)
        except ObjectDoesNotExist:
            prev_article = None
        try:
            next_article = Post.objects.get(id=self.object.id+1)
        except ObjectDoesNotExist:
            next_article = None

        context['prev_article'] = prev_article
        context['next_article'] = next_article
        return context


def post_list(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog.html', {
        'page': page,
        'posts': posts
    })






