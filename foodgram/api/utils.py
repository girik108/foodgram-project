from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response, exception_handler
from rest_framework import status


class FollowError(Exception):
    """Error when user subscribes to himself"""
    pass

class FavoriteError(Exception):
    """Error when user adds his recipes to favotite"""
    pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, ObjectDoesNotExist) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, FollowError) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, FavoriteError) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        
    return response