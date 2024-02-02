from django.urls import path, include
from . import views
from .views import HomePage, DetailPage, CategoryPage, UserDetailView, ProfilePage, ProfileUpdateView,PublishedListView,UnpublishedListView, CreateBlogView

urlpatterns = [
    path("home/", HomePage.as_view(), name="home"),
    path("detail/<slug:slug>/", DetailPage.as_view(), name="detail"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("userProfile/<int:pk>/", ProfilePage.as_view(), name="user_profile"),
    path('updateProfile/<int:pk>/', ProfileUpdateView.as_view(), name='update'),
    path('published/<int:pk>/', PublishedListView.as_view(), name='published_posts'),
    path('unpublished/<int:pk>/', UnpublishedListView.as_view(), name='unpublished_posts'),
    path('create_blog/<int:pk>/', CreateBlogView.as_view(), name='create_blog'),
    path("category/<slug:slug>/", CategoryPage.as_view(), name="category"),
    # path("detail/<slug:slug>/comment/", CommentCreateView.as_view(), name='comment_create'),
    # path("", include('django.contrib.auth.urls')),
   
]