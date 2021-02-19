from recipes.models import Tag


def tag_list(request):

    return {
        'tag_list': Tag.objects.all()
    }