from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password',]

    def validate(self, attrs):

        username_exist = User.objects.filter(username=attrs['username']).exists()
        if username_exist:
            raise serializers.ValidationError(detail="User with username exists")

        email_exist = User.objects.filter(email=attrs['email']).exists()
        if email_exist:
            raise serializers.ValidationError(detail="User with email exists")

        phonenumber_exist = User.objects.filter(phone_number=attrs['phone_number']).exists()
        if phonenumber_exist:
            raise serializers.ValidationError(detail="User with phonenumber exists")

        return super().validate(attrs)



class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id', 'username', 'phone_number']
