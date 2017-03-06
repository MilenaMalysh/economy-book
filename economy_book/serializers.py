from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(source='profile.birthday', required=False)

    class Meta:
        model = User
        fields = ('password','email', 'username', 'birthday')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User()
        user.set_password(validated_data['password'])
        validated_data['password'] = user.password
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)

#
#             #{"username":"ahjsahsld", "email":"asgja@dhsjk.sdhs", "password": "qwerty1995", "birthday": "1995-01-01"}

# from rest_framework import serializers
# from .models import *
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = ('birthday',)
#
#
# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer(required=False)
#
#     class Meta:
#         model = User
#         fields = ('password', 'email', 'username', 'profile')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         user = User.objects.create(**validated_data)
#         Profile.objects.create(user=user, **profile_data)
#         return user


            #{"username":"ahjsahsld", "email":"asgja@dhsjk.sdhs", "password": "qwerty1995", "birthday": "1995-01-01"}
            #{"username":"ahjsahsld", "email":"asgja@dhsjk.sdhs", "password": "qwerty1995", "profile":{"birthday": "1995-01-01"}}