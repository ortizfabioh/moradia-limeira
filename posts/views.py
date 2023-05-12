from operator import index
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Post

class PostListView(ListView):
    template_name = "posts/list.html"

    def post(self, request, *args, **kwargs):
        return index(request)

    def get_queryset(self, *args, **kwargs):
        path = self.request.get_full_path()
        repuPath = True if path == '/posts/republicas' else False
        return Post.objects.filter(repuPost=repuPath)

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = "posts/detail.html"
