from django.db.models import Q


def get_tag_filter(request):
    # получаем информацию по выбраным тегам
    tags = request.GET.get('tags', 'breakfast,dinner,supper')
    tags = tags.split(',')
    # случай когда не выбран ни один тег
    if tags == ['']:
        tags = ['None']
    # генерируем фильтр по тегам
    tag_filter = Q(tags__contains=tags[0])
    for tag in tags[1:]:
        tag_filter |= Q(tags__contains=tag)
    return tag_filter, tags
