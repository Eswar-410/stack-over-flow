from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('logout/', logout_user, name='logout'),


]
