from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Profile, Product, CustomUser, Meson, Category, Order, ItemOrder


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
        order = Order.objects.create(user=user)
        order.save()
        token = Token.objects.create(user=user)
        token.save()
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

    def validate(self, data):
        if data['event_start'] > data['event_end']:
            raise serializers.ValidationError("finish must occur after start")


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


class ItemOrderSerializer(serializers.ModelSerializer):
    cost = serializers.ReadOnlyField()

    class Meta:
        model = ItemOrder
        fields = ['product', 'price', 'count', 'cost']
        extra_kwargs = {'price': {'read_only': True}}

    def to_representation(self, instance):
        data = super(ItemOrderSerializer, self).to_representation(instance)
        data['product'] = ProductSerializer(instance=instance.product).data
        data['order'] = OrderSerializer(instance=instance.order).data

        return data

    def create(self, validated_data):
        obj = ItemOrder.objects.create(**validated_data)
        return obj


class OrderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    cost = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'items', 'cost', 'paid']
        extra_kwargs = {'items': {'read_only': True}}

    # def to_representation(self, instance):
    #     data = super(OrderSerializer, self).to_representation(instance)
    #     print(data['items'])
    #     list_item = []
    #     for item in data['items']:
    #         item_order = ItemOrder.objects.filter(pk=item).values()
    #         print(item_order)
    #         obj_product = Product.objects.get(pk=item_order[0]['product_id'])
    #         list_item.append(ProductSerializer(instance=obj_product).data)
    #         list_item.append(item_order[0]['count'])
    #
    #     data['items'] = list_item
    #     return data



