from django.template import Library


register = Library()


@register.filter()
def enumer(some):
    return list(enumerate(some, 1))
