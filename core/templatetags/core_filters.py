from django.template import Library
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