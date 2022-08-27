from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from .serializers import RegisterSerializer, SoftdeskObtainPairSerializer


class SoftdeskTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = SoftdeskObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
