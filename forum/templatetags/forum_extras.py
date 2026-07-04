from django import template

register = template.Library()


@register.filter
def is_moderator(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Moderators').exists()