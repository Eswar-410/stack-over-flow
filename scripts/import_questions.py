# scripts/import_questions.py

import os
import sys
import django
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stack_over_flow.settings")
django.setup()

from questions.models import Question, QuestionComment, Answer, AnswerComment

with open(os.path.join(BASE_DIR, 'stack_data.json')) as f:
    data = json.load(f)

for item in data:
    question = Question.objects.create(
        title=item['title'],
        body=item['body'],
        questioned_by=item['questioned_by'],
        no_of_votes=item['no_of_votes'],
        tags=item['tags']
    )

    for question_comment_data in item.get('question_comments', {}).values():
        QuestionComment.objects.create(
            question=question,
            commented_message=question_comment_data['commented_message'],
            commented_by=question_comment_data['commented_by']
        )

    for answer_data in item.get('answers', {}).values():
        answer = Answer.objects.create(
            question=question,
            answer=answer_data['answer'],
            answered_by=answer_data['answered_by'],
            answer_votes=answer_data['answer_votes']
        )

        for answer_comment_data in answer_data.get('comments', {}).values():
            AnswerComment.objects.create(
                answer=answer,
                commented_message=answer_comment_data['commented_message'],
                commented_by=answer_comment_data['commented_by']
            )
