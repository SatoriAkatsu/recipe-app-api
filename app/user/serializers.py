"""
Serializers for the user API View.
"""
from django.contrib.auth import (get_user_model)
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # トークンを作成

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )


class RetrieveUpdateSerializer(serializers.ModelSerializer):
    """TODO メールアドレス変更後の対策
        1. 変更確認メールの送信:
            メールアドレス変更後に確認のためのメールを送信し、
            ユーザーがその変更を承認する仕組みを導入することが推奨されます。
            これにより、メールアドレスの変更が正当であることを確認できます。

        2. ユーザーへの通知:
            メールアドレスが変更されたことをユーザーに通知することで、
            重要な情報が届かない問題を防ぎます。

        3. セキュリティ対策:
            メールアドレスの変更はセキュリティ上重要な操作であるため、
            変更の際には適切な認証や検証を行い、
            ユーザーの同意を確認することが重要です。
    """
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')

    def update(self, instance, validated_data):
        """Update and return user."""
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        # 他のフィールドを更新
        user = super().update(instance, validated_data)

        # メールアドレスが提供されている場合、ユニーク制約の確認
        if email is not None:
            if get_user_model() \
                .objects.filter(email=email) \
                    .exclude(pk=instance.pk).exists():
                msg = _('This email address is already in use.')
                raise serializers.ValidationError(msg)

            user.email = email

        # パスワードが提供されている場合は設定
        if password is not None:
            user.set_password(password)

        # メールアドレスとパスワードのいずれか、または両方の変更を保存
        user.save()

        return user
