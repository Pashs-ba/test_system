from django.template import Library
from core.models import Problems
register = Library()

@register.filter()
def messages_tag(tag):
    bootstrap_tag = {
        'error': 'danger',
        'info': 'info',
        'success':'success',
        'warning':'warning'
    }
    return bootstrap_tag[tag]

@register.simple_tag 
def count_new_errors():
    return len(Problems.objects.filter(is_ansed=False))