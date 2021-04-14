from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'misc/404.html',
                  {'path': request.build_absolute_uri()}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'misc/403.html',
                  {'path': request.build_absolute_uri()}, status=403)
