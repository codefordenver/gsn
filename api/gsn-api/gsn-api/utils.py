from user_app.serializers import CustomUserSerializer

def my_jwt_response_handler(token, user=None, request=None):
  return{
    'token': token,
    'user': CustomUserSerializer(user, context={'request': request}).data
  }
