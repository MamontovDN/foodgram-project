def shop_list_count(request):
    if not request.user.is_authenticated:
        return {}
    return {'shop_list_count': request.user.shop_list.count()}
