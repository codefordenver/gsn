from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, SpecialKeyLogList
from .models import SpecialKeyLog
from uuid import uuid4
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
# Create your views here.


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a method here too, for retrieving a list of all User objects.

    This requires a secret key to be submitted that way registration is limited to those with a key.
    The key can be created with the SpecialKey view
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        json = request.data

        if "special_key" in json.keys():
            special_key = json["special_key"]
        else:
            return Response({
                                "Sorry": "A registration key is required. Please get a registration key from an existing account."
                            })
        current_time = timezone.now()
        hours_24_before_now = current_time - timedelta(hours = 24)

        special_key_log = SpecialKeyLog.objects.filter(special_key = special_key, created__range=[hours_24_before_now,current_time])

        if special_key_log.count() > 0:
            user_data = {
                "username": json["username"],
                "password": json["password"]
            }
            serializer = UserSerializerWithToken(data = user_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                                "Sorry": "The registration key has either expired or does not exist. If you believe this is an error, please try again. Otherwise, please request a registration key from an existing user."
                            })


class SpecialKey(generics.ListCreateAPIView):

    def get(self, request, format = None):
        user = User.objects.get(username = request.user.username)
        current_time = timezone.now()
        hours_24_before_now = current_time - timedelta(hours = 24)
        queryset = SpecialKeyLog.objects.filter(user_that_create_request = user, created__range=[hours_24_before_now,current_time])
        serializer = SpecialKeyLogList(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        """
        This method allows a secret key to be created by authenticated users. The secret key can then be
        used by people wanting to register within 24 hours.
        """

        try:

            if request.user.is_authenticated():
                special_key = uuid4()
                user = User.objects.get(username=request.user.username)
                SpecialKeyLog.objects.create(special_key = special_key, user_that_create_request=user)
                return HttpResponseRedirect(f"/user_app/special-key/")
            else:
                raise PermissionDenied()
        except Exception as e:
            return Response({
                                "Sorry": "The database was not able to create this secret key.",
                                "The attempt raised the following errors": str(e)
                            })
