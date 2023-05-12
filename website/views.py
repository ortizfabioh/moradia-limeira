from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NewPostForm
from posts.models import PostImages, Post
from django.contrib import messages

# Validação do formulário de posts
def form_page(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('image')
        if form.is_valid():
            print(form.cleaned_data)
            author = form.cleaned_data["author"].strip('\n')
            description = form.cleaned_data["description"].strip('\n')
            contact_info = form.cleaned_data["contact_info"].strip('\n') if form.cleaned_data["contact_info"] else ''
            repuPost = form.cleaned_data["repuPost"]
            data = Post.objects.create(author=author, description=description, contact_info=contact_info, repuPost=repuPost)
            for f in files:
                PostImages.objects.create(post=data, images=f)
            messages.warning(request, "A sua postagem foi criada e será analisada por um moderador dentro de 2 dias.\nCaso seja aprovada, ela aparecerá no feed do nosso site." )
            return HttpResponseRedirect("/form/")
    else:
        form = NewPostForm()

    return render(request, "form/view.html", {"form": form})
