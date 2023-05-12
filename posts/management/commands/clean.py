from django.core.management.base import BaseCommand
from posts.models import Post

class Command(BaseCommand):
    help = "Clean unaccepted posts"
    
    def handle(self, *args, **options):
        Post.objects.filter(accepted=False).delete()
        print('Cleaned')