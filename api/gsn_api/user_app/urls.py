from django.urls import path
from .views import current_user, UserList, SpecialKey

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('special-key/', SpecialKey.as_view())
]
