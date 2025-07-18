from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='home'),
    path('navbar/', navbar, name='nav'),
    path('question/', question, name='question'),
    path('data/', form_data, name='data'),
    path('profile/', profile, name='profile'),
    path('tags/', tags, name='tags'),
    path('tag_questions/', tag_questions, name='tag_questions'),
    path('question_analysis/<int:pk>/', question_analysis, name='analysis'),
    path('upvote/', upvote, name='upvote'),
    path('downvote/', downvote, name='downvote'),
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('answer_upvote/<int:pk>/', answer_upvote, name='answer_upvote'),
    path('answer_downvote/<int:pk>', answer_downvote, name='answer_downvote'),
    path('answer_comment/<int:pk>/', add_answer_comment, name='add_answer_comment'),
    path('add_answer/<int:pk>/', add_answer, name='add_answer'),
    path('questions/', questions, name='questions'),






]
