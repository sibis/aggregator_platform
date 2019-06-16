from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from django.core.exceptions import ObjectDoesNotExist


def is_store_manager(func):
    def func_wrapper(request, *args, **kwargs):
        user_type = request.user.user_type
        if user_type == 1:
            return func(request, *args, **kwargs)
        return Response({'msg':'You are not authorized to take this action'}, status=status.HTTP_401_UNAUTHORIZED)
    return func_wrapper


def is_delivery_person(func):
    def func_wrapper(request, *args, **kwargs):
        user_type = request.user.user_type
        if user_type == 2:
            return func(request, *args, **kwargs)
        return Response({'msg':'You are not authorized to take this action'}, status=status.HTTP_401_UNAUTHORIZED)
    return func_wrapper