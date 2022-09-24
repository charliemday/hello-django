from beaconclient.beacon import Beacon
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from .models import User, UserFeedback
from .serializers import UserSerializer, LoginSerializer

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailsView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserFeedbackView(APIView):
    def post(self, request):
        user = request.user
        feedback = request.data.get("feedback")
        if feedback:
            UserFeedback.objects.create(user=user, feedback=feedback)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Feedback is required"},
            )

