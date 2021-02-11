from django import template
from django.shortcuts import get_object_or_404
from registration.forms import User

register = template.Library()


@register.filter
def minus(num1, num2):
    return num1 - num2


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def add_param(tags, val):
    param = list(tags)
    if val not in tags:
        param.append(val)
    return ','.join(param)


@register.filter
def del_param(tags, val):
    param = list(tags)
    if val in tags:
        param.remove(val)
    return ','.join(param)


@register.filter
def get_param(tags):
    return ','.join(tags)


@register.filter
def favorites(rec_id, username):
    user = get_object_or_404(User, username=username)
    return user.favorites.filter(recipe=rec_id).exists()


@register.filter
def subscribes(auth_id, username):
    user = get_object_or_404(User, username=username)
    return user.subscribes.filter(author__id=auth_id).exists()


@register.filter
def purchase(rec_id, username):
    user = get_object_or_404(User, username=username)
    return user.shop_list.filter(recipe=rec_id).exists()


@register.filter
def split(string):
    strings = string.split('\n')
    return strings
