from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'user': request.user}
    return render(request, 'core/index.html', context=context)
