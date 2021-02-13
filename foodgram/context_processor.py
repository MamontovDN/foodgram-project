def shop_list_count(request):
    if not request.user.is_authenticated:
        return {}
    count = request.user.shop_list.count()
    if count > 0:
        return {'shop_list_count': count}
    else:
        return {}
