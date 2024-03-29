
from django.contrib.auth import authenticate, user_logged_in

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from app.models import Profile
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            print(self.context['request'])
            user = authenticate(request=self.context['request'], **credentials)
            print(user)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__,
                                    request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class RegisterSerializer(serializers.ModelSerializer):

    # username = serializers.CharField(
    #         validators=[UniqueValidator(queryset=User.objects.all())]
    #         )
    # password = serializers.CharField(write_only=True)

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'],
    #          validated_data['password'])
    #     return user
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'password')

class Profile(serializers.ModelSerializer):
    profile = RegisterSerializer(required=True)
    class Meta:
        model=Profile
        fields=('school_name','Company_name','Current_Location')
    