from rest_framework import serializers
from .models import Profile, Product, CustomUser, Meson, Category


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(name=validated_data['name'],
                                              email=validated_data['email'],
                                              phone=validated_data['phone'],
                                              password=validated_data['password'])
        user.set_password(validated_data['password'])
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'size', 'color', 'number', 'price', 'meson', 'categories']

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data['meson'] = MesonSerializer(instance=instance.meson).data
        data['categories'] = CategorySerializer(instance=instance.categories).data
        return data

