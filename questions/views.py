from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Sum
from django.urls import reverse

# Create your views here.


def home(request):
    questions_data = Question.objects.all()
    return render(request, 'home.html', {'questions_data': questions_data})


def questions(request):
    questions_data = Question.objects.all()

    return render(request, 'question_main_page.html', {'questions_data': questions_data})


def navbar(request):
    return render(request, 'partials/navbar.html')


@login_required
def question(request):
    return render(request, 'question.html')


def form_data(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.get('tags')
        tags = [tag.strip() for tag in tags.split(',')]

        Question.objects.create(
            title=title,
            body=body,
            tags=tags,
            no_of_votes=0,
            questioned_by=request.user.username
        )
        return redirect('home')

    else:
        return redirect('question')


@login_required
def profile(request):
    user = request.user

    # Follow logic

    follow_id = request.GET.get('follow')
    if follow_id:
        question = get_object_or_404(Question, id=follow_id)
        Follow.objects.get_or_create(user=user, question=question)

    # General user stats
    questions = Question.objects.filter(questioned_by=user.username)
    question_votes = questions.aggregate(Sum('no_of_votes'))[
        'no_of_votes__sum'] or 0
    questions_count = questions.count()

    answers = Answer.objects.filter(answered_by=user.username)
    answer_votes = answers.aggregate(Sum('answer_votes'))[
        'answer_votes__sum'] or 0
    answers_count = answers.count()

    question_comments = QuestionComment.objects.filter(
        commented_by=user.username)
    question_comments_count = question_comments.count()

    answer_comments = AnswerComment.objects.filter(commented_by=user.username)
    answer_comments_count = answer_comments.count()

    following_cards = Question.objects.filter(follow__user=user)

    context = {
        'question_votes': question_votes,
        'questions_count': questions_count,
        'answer_votes': answer_votes,
        'answers_count': answers_count,
        'question_comments_count': question_comments_count,
        'answer_comments_count': answer_comments_count,
        'following_cards': following_cards,
    }

    return render(request, 'profile.html', context)


def tags(request):
    method_tags = {}
    filtered_tags = {}

    if request.method == 'POST':
        tag_name = request.POST.get('search-tag')
    else:
        tag_name = ''
    objects = Question.objects.all()

    for object in objects:
        for tag in object.tags:

            if tag not in method_tags:
                method_tags[tag] = 1
            else:
                method_tags[tag] += 1

    if request.method == 'POST':

        for tag in method_tags:

            if tag.startswith(tag_name):
                filtered_tags[tag] = method_tags[tag]

        return render(request, 'tags.html', {'tags': filtered_tags})

    return render(request, 'tags.html', {'tags': method_tags})


def tag_questions(request):
    tag = request.GET.get('tag')

    questions = Question.objects.filter(tags__contains=[tag])
    questions_count = questions.count()

    return render(request, 'question_page.html', {'questions_data': questions, 'tag': tag, 'questions_count': questions_count})


@login_required
def question_analysis(request, pk):
    question_details = Question.objects.get(pk=pk)
    question_comments = QuestionComment.objects.filter(question=pk)
    answer_details = Answer.objects.filter(question=pk)
    answer_comments = AnswerComment.objects.filter(answer__question=pk)

    print(answer_details)

    context = {
        'question_details': question_details,
        'question_comments': question_comments,
        'answer_details': answer_details,
        'answer_comments': answer_comments
    }

    return render(request, 'question_analysis.html', context)


def upvote(request):
    user = request.user
    vote_count = int(request.GET.get('upvote'))
    vote_id = int(request.GET.get('upvote_id'))
    question = get_object_or_404(Question, id=vote_id)

    vote, created = Vote.objects.get_or_create(
        user=user, question=question, defaults={'is_upvote': True})

    if created:
        vote.is_upvote = True
        question.no_of_votes = vote_count + 1
    else:
        if vote.is_upvote is False:
            vote.is_upvote = True
            question.no_of_votes = vote_count + 2
        else:
            return redirect(reverse('analysis', kwargs={'pk': vote_id}))

    vote.save()
    question.save()

    return redirect(reverse('analysis', kwargs={'pk': vote_id}))


def downvote(request):
    user = request.user
    vote_count = int(request.GET.get('downvote'))
    vote_id = int(request.GET.get('downvote_id'))
    question = get_object_or_404(Question, id=vote_id)

    vote, created = Vote.objects.get_or_create(
        user=user, question=question, defaults={'is_upvote': False})

    if created:
        question.no_of_votes = vote_count - 1
        vote.is_upvote = False
    else:
        if vote.is_upvote is True:
            question.no_of_votes = vote_count - 2
            vote.is_upvote = False
        else:
            return redirect(reverse('analysis', kwargs={'pk': vote_id}))

    vote.save()
    question.save()

    return redirect(reverse('analysis', kwargs={'pk': vote_id}))


def add_comment(request, pk):

    commented_message = request.POST.get('manual-comment')
    commented_by = request.user

    QuestionComment.objects.create(
        question_id=pk,
        commented_message=commented_message,
        commented_by=commented_by
    )
    url = reverse('analysis', kwargs={'pk': pk})

    return redirect(url)


def answer_upvote(request, pk):
    user = request.user
    vote_count = int(request.GET.get('upvote'))
    vote_id = int(request.GET.get('upvote_id'))
    answer = get_object_or_404(Answer, id=vote_id)

    vote, created = Vote.objects.get_or_create(
        user=user, answer=answer, question=None, defaults={'is_upvote': True})

    if created:
        answer.answer_votes = vote_count + 1
        vote.is_upvote = True
    else:
        if vote.is_upvote is False:
            answer.answer_votes = vote_count + 2
            vote.is_upvote = True
        else:
            return redirect(reverse('analysis', kwargs={'pk': pk}))

    vote.save()
    answer.save()

    return redirect(reverse('analysis', kwargs={'pk': pk}))


def answer_downvote(request, pk):
    user = request.user
    vote_count = int(request.GET.get('downvote'))
    vote_id = int(request.GET.get('downvote_id'))
    answer = get_object_or_404(Answer, id=vote_id)

    vote, created = Vote.objects.get_or_create(
        user=user, answer=answer, question=None, defaults={'is_upvote': False})

    if created:
        answer.answer_votes = vote_count - 1
        vote.is_upvote = False
    else:
        if vote.is_upvote is True:
            answer.answer_votes = vote_count - 2
            vote.is_upvote = False
        else:
            return redirect(reverse('analysis', kwargs={'pk': pk}))

    vote.save()
    answer.save()

    return redirect(reverse('analysis', kwargs={'pk': pk}))


def add_answer_comment(request, pk):
    commented_message = request.POST.get('manual-comment')
    commented_by = request.user

    AnswerComment.objects.create(
        answer_id=pk,
        commented_message=commented_message,
        commented_by=commented_by
    )
    question_id = request.POST.get('question_id')

    url = reverse('analysis', kwargs={'pk': question_id})

    return redirect(url)


def add_answer(request, pk):
    answer = request.POST.get('manual-answer')

    Answer.objects.create(
        question_id=pk,
        answer=answer,
        answered_by=request.user,
        answer_votes=0,
    )

    url = reverse('analysis', kwargs={'pk': pk})

    return redirect(url)
