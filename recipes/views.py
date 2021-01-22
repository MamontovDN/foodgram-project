from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'indexAuth.html')
    else:
        return render(request, 'indexNotAuth.html')
