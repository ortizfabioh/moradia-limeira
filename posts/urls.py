from django.urls import path
from .views import PostListView, PostDetailView

app_name='posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('republicas', PostListView.as_view(), name='repuList'),
    path('republicas/<slug:slug>/', PostDetailView.as_view(), name='repuDetail'),
]