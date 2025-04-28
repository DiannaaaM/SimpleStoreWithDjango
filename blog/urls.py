from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostDeleteView, PostCreateView, PostUpdateView, PostDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path("", PostListView.as_view(), name="posts_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="posts_detail"),
    path("create", PostCreateView.as_view(), name="posts_create"),
    path("<int:pk>/update", PostUpdateView.as_view(), name="posts_update"),
    path("<int:pk>/delete", PostDeleteView.as_view(), name="posts_delete"),
]
