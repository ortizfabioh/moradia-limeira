from django import forms
from posts.models import Post

# Definição dos campos do formulário de posts
class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'description', 'contact_info', 'repuPost', 'image')
        labels = {
            'author': 'Seu nome ',
            'description': 'Sua postagem ',
            'contact_info': 'Informação de contato',
            'repuPost': 'Esta vaga é em uma República Universitária?',
            'image': 'Tem alguma foto do local?'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
            'contact_info': forms.TextInput(attrs={'class': 'col-md-5'})
        }