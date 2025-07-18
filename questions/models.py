from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    questioned_by = models.CharField(max_length=100, blank=True)
    no_of_votes = models.IntegerField()
    tags = ArrayField(models.CharField(
        max_length=50), blank=True, default=list)

    def __str__(self):
        return self.title


class QuestionComment(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='question_comments')
    commented_message = models.TextField()
    commented_by = models.CharField(max_length=100)

    def __str__(self):
        return self.commented_message


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    answered_by = models.CharField(max_length=100)
    answer_votes = models.IntegerField()

    def __str__(self):
        return self.answer


class AnswerComment(models.Model):
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='comments')
    commented_message = models.TextField()
    commented_by = models.CharField(max_length=100)

    def __str__(self):
        return self.commented_message


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} follows '{self.question.title}'"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('user', 'question', 'answer')
