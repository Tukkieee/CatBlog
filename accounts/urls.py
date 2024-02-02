from django.urls import path, include
from . import views
from .views import RegisterView, SignInView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("", include('django.contrib.auth.urls')),
]
