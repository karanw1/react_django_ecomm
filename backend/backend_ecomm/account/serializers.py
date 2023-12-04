from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User



    
    
class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
                                required=True,
                                validators=[UniqueValidator(queryset=User.objects.all(),message='this email already exists!')]
                                )
    password = serializers.CharField(write_only=True, required=True)

    
    class Meta:
        model = User
        fields = ('email', 'password','first_name','last_name')

    def create(self, validated_data):
        return  User.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name')
    
    
         

class LogoutSerializer(serializers.Serializer):

    refresh=serializers.CharField(write_only=True, required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'username or password does not matched.'
    }

    def validate(self, attrs):
            data = super().validate(attrs)
            data["user_data"] = UserDetailSerializer(self.user).data
            return data
    