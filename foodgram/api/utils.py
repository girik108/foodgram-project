from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response, exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, ObjectDoesNotExist) and not response:
        response = Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
        
    return response