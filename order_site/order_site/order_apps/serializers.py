from rest_framework import serializers
from .models import Profile, Product, CustomUser, Meson, Category


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'read_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(name=validated_data['name'],
                                              email=validated_data['email'],
                                              phone=validated_data['phone'])
        user.set_password(password=validated_data['password'])
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'code_postie', 'address']


class MesonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meson
        fields = ['name', 'city', 'address', 'email', 'event_start', 'event_end']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'size', 'color', 'number', 'price', 'meson', 'categories']
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['name']


