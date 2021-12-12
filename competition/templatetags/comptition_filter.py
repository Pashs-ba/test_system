from django.template import Library
from core.models import QuestionAns


register = Library()


@register.filter()
def enumer(some):
    return list(enumerate(some, 1))

@register.filter
def check_ans_id(user, question):
    if QuestionAns.objects.filter(user=user, question=question):

        return QuestionAns.objects.filter(user=user, question=question).order_by('date')[0].result
    else:
        return -1