from django.db.models import QuerySet
from django.template import Library
from core.models import Question, QuestionAns, VariantQuestionGenerator, VariantQuestion
from django.db.models import Count

register = Library()


@register.filter(name='get_type_name')
def get_type_name(type_num: str):
    for i in Question.QUESTION_TYPE:
        if i[0] == type_num:
            return i[1]
    return 'Not found'

@register.filter
def get_widget_type(obj):
    return obj.__class__.__name__

@register.filter
def count_variants(pk):
    return VariantQuestionGenerator.objects.annotate(variant_count=Count('variantquestion')).get(pk=pk).variant_count

@register.filter
def occ_variants(pk):
    return len(VariantQuestion.objects.filter(generator=VariantQuestionGenerator.objects.get(pk=pk), user__isnull=False))
