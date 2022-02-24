from .models import Genre

def get_category(request):
    genres = Genre.objects.all()
    context = {'genres':genres}
    return context