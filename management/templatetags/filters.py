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



