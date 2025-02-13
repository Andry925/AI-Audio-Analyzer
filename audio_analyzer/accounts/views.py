from django.contrib.auth import login, get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, UserLoginSerializer, CurrentUserSerializer

UserCustomModel = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not (serializer.is_valid(raise_exception=True)
                and not request.user.is_authenticated):
            return Response(
                data={"detail": "You are already logged in."},
                status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(request.data)
        if user:
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        response_data = {}
        serializer = UserLoginSerializer(data=request.data)
        if not (serializer.is_valid(raise_exception=True)
                and not request.user.is_authenticated):
            return Response(
                data={"detail": "You are already logged in."},
                status=status.HTTP_400_BAD_REQUEST)
        user = serializer.authenticate_user(request_data=request.data)
        if user:
            token = RefreshToken.for_user(user)
            response_data['tokens'] = {
                'refresh': str(token), 'access': str(token.access_token)
            }
            login(request, user)
            return Response(data=response_data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'You have successfully logged out'},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user_data = UserCustomModel.objects.get(id=request.user.id)
        serializer = CurrentUserSerializer(user_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
