from django.core.management.base import BaseCommand
import time, re
from posts.models import Post
from tags.models import Tag
from facebook_scraper import get_posts
from unidecode import unidecode

class Command(BaseCommand):
    help = "Collect posts from Facebook"
    
    def handle(self, *args, **options):
        groups = {
            'Moradia UNICAMP Limeira': 448106555248538,
            'Moradia Limeira Unicamp FT-FCA': 1444273352541572
        }
        percentile = 0.45  # How much a post's words have to match the tags 
        tags = [tag.title for tag in list(Tag.objects.all())]
        stopwords = ('as','às','os','ao','aos','de','do','dos','da','das','no','nos','na','nas','pelo','pelos','pela','pelas','um','uns','uma','umas','num','numa',
                    'por','para','pra','pro','me','te','tu','ti','que','já','ja','você','voce','vc','se','em','só','ou','seu','sua','meu','minha','meus','minhas',
                    'este','deste','neste','aqui','aq','aquilo','daquilo','naquilo','aquele','daquele','naquele','aquela','daquela','naquela','com','sem','ola','olá','oi','ooi','oii'
                    'oie','quem','qual','qualquer','todo','toda','todos','todas','td','tds','este','esta','estas','estas','também','tb','tbm','lá','la','cá','muito','mt','mto',
                    'não','nao','sim','ele','eles','ela','elas','essa','essas','esse','esses','dessa','dessas','desse','desses','alô','alo','bem','bom','boa',
                    'era','eram','há','ser','seria','seriam','serão','sou','somos','seremos','seja','sejam','haveria','haveriam','houveram','houve','estão','está',
                    'estamos','estaremos','foi','for','fosse','foram','fomos','tem','temos','teriam','teriamos','teríamos','terão','tive','tivemos','tiveram','teremos','tenha','tenham')
        ng_words = ('[procuro]','[procurando]','[procura]','procuro', 'procurando')  # If a post has any of these words, it's not accepted
        
        try:
            for group in groups:
                print(f'LENDO POSTS DO GRUPO "{group}"')

                # Gets 50 posts per group each run
                for post_fb in get_posts(group=groups[group], pages=5, options={'posts_per_page': 10, 'allow_extra_requests': False}, cookies='cookies.txt'):
                    time.sleep(0.7)
                    
                    # Ignore posts with ng_words
                    if any([x.lower() in post_fb['post_text'].lower() for x in ng_words]) or post_fb['post_text'] == None:
                        continue

                    post = {
                        'id': post_fb['post_id'],
                        'idUser': post_fb['user_id'],
                        'author': post_fb['username'],
                        'description': post_fb['post_text'].replace('\r', '').strip(),
                        'datePost': post_fb['time'],
                        'images': post_fb['images'],
                        'factcheck': post_fb['factcheck'],
                        'link': post_fb['link'],
                        'url': post_fb['post_url'],
                        'available': post_fb['available'],
                    }

                    if post['description']:  # Check if description it's empty
                        # remove emojis and special characters, and even replaces punctuated letters with their normal one
                        description = re.sub('[^a-zA-Z0-9 ]+', '', remove_emoji(unidecode(post['description'].lower()))).strip()

                        # split and remove stopwords from text
                        text = description.split(' ')
                        clean_text = []
                        for word in text:
                            if (word.lower() not in stopwords) and ((word.lower().isalnum()) and (not word.lower().isnumeric()) and (len(word)>1)):
                                clean_text.append(word)  # clean_text is the list of words to be analyzed

                        words = list(dict.fromkeys(clean_text))  # Remove duplicate words

                        if len(words) <= 3: continue  # Don't consider a full sentence if it has less than 3 words 
                        
                        # Count words in post that are tags
                        hits = 0
                        for word in words:
                            if word.lower().strip() in [tag.lower().strip() for tag in tags]:
                                hits += 1

                        repuPost = True if any(x in words for x in ['republicas','republica','rep']) else False
                        if (hits >= (len(words)*percentile) or repuPost) and post['available']:
                            # Don't let it insert duplicate posts by comparing the description with existing posts
                            if not any(post['description']==p for p in [exist_post.description.split('<a')[0].strip() for exist_post in list(Post.objects.all())]):    
                                Post.objects.create(
                                    author=post['author'], 
                                    description=f"{post['description']}\n\n<a href={post['url']} target='_blank'>Post original no Facebook</a>", 
                                    datePost=post['datePost'], 
                                    repuPost=repuPost, 
                                    fbPost=True, 
                                    accepted=False
                                )
        
        except KeyboardInterrupt:
            print('Serviço parado pelo usuário')

def remove_emoji(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
