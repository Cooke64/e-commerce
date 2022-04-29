from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services import send_email
from customer.models import User
from .serializers import UserSerializer, LoginUserSerializer, \
    ConformationCodeSerializer
from .services import get_tokens_for_user


class UserSingUpApiView(APIView):
    """Вью для отображения регистрации пользователя и
    отправки сообщения на указанный mail кода подтверждения.
    """
    queryset = get_user_model()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            serializer.save()
            return JsonResponse({'email': email, 'username': username})


class TokenAPIView(APIView):
    """Вью для подтверждения полного доступа к
    сайту зарегистрированного пользователя.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ConformationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                username = serializer.validated_data['username']
                code = serializer.data['confirmation_code']
            except ValueError as e:
                raise e
            user = get_object_or_404(User, username=username)
            if code == user.confirmation_code:
                token = get_tokens_for_user(user)
                user.is_active = True
                user.save()
                return JsonResponse({'token': token}, status=OK_STATUS)
            return JsonResponse(
                {'Статус': 'Неверный код подтверждения'}, status=BAD_STATUS)