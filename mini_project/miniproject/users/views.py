

from rest_framework import generics

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import User
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
