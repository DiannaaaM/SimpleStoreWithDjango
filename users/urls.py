from django.urls import path
from .views import register, EmailLoginView, user_logout

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
]
