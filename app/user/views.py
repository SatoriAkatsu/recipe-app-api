"""
Views for the user API.
"""
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from drf_spectacular.utils import (
    extend_schema, OpenApiResponse
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import (
        RegisterSerializer,
        LoginSerializer,
        RetrieveUpdateSerializer,
    )


class RegisterView(APIView):
    """Create a new user in the system."""
    @extend_schema(
        request=RegisterSerializer,
        responses={200: RegisterSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response(
                    {'token': token.key}, status=status.HTTP_201_CREATED
                )
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class AuthToken(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                        {'token': token.key}, status=status.HTTP_200_OK
                    )
            else:
                msg = _('Invalid email or password.')
                return Response(
                        {'error': msg}, status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class RetrieveUpdateView(APIView):
    authentication_classes = [TokenAuthentication]  # トークン認証を使用
    permission_classes = [IsAuthenticated]  # 認証済みユーザーのみアクセス許可

    @extend_schema(
        responses={200: RetrieveUpdateSerializer},
        description="ユーザー情報を取得します。"
    )
    def get(self, request):
        # GETリクエストでユーザー情報を取得
        serializer = RetrieveUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=RetrieveUpdateSerializer,
        responses={
            200: RetrieveUpdateSerializer,
            400: OpenApiResponse(
                description='リクエストデータのバリデーションエラー。'
            )
        },
        description="ユーザー情報を部分的に更新します。"
    )
    def patch(self, request):
        serializer = RetrieveUpdateSerializer(
                request.user, data=request.data, partial=True
            )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'email': user.email}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
