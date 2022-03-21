from django.template import Library
from core.models import QuestionAns, Question
from ast import literal_eval
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

@register.filter
def get_vaule(dict, key):
    return dict[key]

@register.filter
def is_ansed(question: Question, user):
    return bool(QuestionAns.objects.filter(user=user, question=question))

@register.filter
def get_ans(question: Question, user):
    print(QuestionAns.objects.filter(user=user, question=question)[0].ans)
    return QuestionAns.objects.filter(user=user, question=question)[0].ans

@register.filter
def count_ans(competition, user):
    c = 0
    for i in competition.questions.all():
        c+= len(QuestionAns.objects.filter(user=user, question=i))
    return c


@register.filter
def get_question_ans(a):
    # print(QuestionAns.objects.filter(user=user, question=question)[0].ans)
    return literal_eval(a).get('ans', 'error')
@register.filter
def is_right(question: Question, user):
    ans = QuestionAns.objects.filter(user=user, question=question)
    if ans:
        return ans[0].result
@register.filter
def count_true(competition, user):
    count = 0
    for i in QuestionAns.objects.filter(user=user, question__in=competition.questions.all()):
        if i.result:
            count+=1
    return count
