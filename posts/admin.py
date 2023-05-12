from django.contrib import admin
from .models import Post, PostImages

@admin.action(description='Aceitar posts selecionados')
def accept_posts(modelAdmin, request, queryset):
    queryset.update(accepted=True)

@admin.action(description='Rejeitar posts aceitos')
def reject_posts(modelAdmin, request, queryset):
    queryset.update(accepted=False)

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_description', 'datePost', 'repuPost', 'fbPost', 'accepted')
    actions = [accept_posts, reject_posts]
    class Meta:
        model = Post

    def get_description(self, obj):
        max_len = 150
        return obj.description if len(obj.description) < max_len else (obj.description[:max_len-2] + '..')
    get_description.short_description = "description"


class PostImagesAdmin(admin.ModelAdmin):
    class Meta:
        model = PostImages

admin.site.register(Post, PostAdmin)
admin.site.register(PostImages, PostImagesAdmin)