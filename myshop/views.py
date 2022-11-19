from django.shortcuts import render, redirect

def page_not_found_view(request, *args, **argv):
    return render(request, 'main/404.html')


def page_not_found_view_500(request, *args, **argv):
    return render(request, 'main/404.html')
