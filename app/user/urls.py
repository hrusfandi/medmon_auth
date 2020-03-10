from django.urls import path
from user.views import UserView, UserDetailView

from rest_framework_simplejwt.views import TokenObtainPairView, \
                                           TokenRefreshView, \
                                           TokenVerifyView


app_name = 'user'

urlpatterns = [
    path('users/', UserView.as_view(), name='user_list'),
    path('detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
