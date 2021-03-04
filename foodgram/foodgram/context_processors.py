from recipes.models import Tag


def tag_list(request):

    return {
        'tag_list': Tag.objects.all()
    }
    

def tag_get(request):
    tag = request.GET.get('tag')
    result = ''
    if tag:
        result = f'&tag={tag}'
    return {
        'tag_get': result
    }
