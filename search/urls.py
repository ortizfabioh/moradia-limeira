from django.urls import path
from .views import SearchPostView

app_name = "search"

urlpatterns = [
    path('', SearchPostView.as_view(), name='query'),
]