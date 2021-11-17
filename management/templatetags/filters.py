from django.db.models import QuerySet
from django.template import Library
from core.models import Question, QuestionAns

register = Library()


@register.filter(name='get_type_name')
def get_type_name(type_num: str):
    for i in Question.QUESTION_TYPE:
        if i[0] == type_num:
            return i[1]
    return 'Not found'


@register.filter
def check_ans_id(user, question):
    if QuestionAns.objects.filter(user=user, question=question):

        return QuestionAns.objects.filter(user=user, question=question).order_by('date')[0].result
