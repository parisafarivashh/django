from django.contrib import admin
from django.db.models import Count
from .models import Product, Profile, Category, CustomUser, Meson, Order,ItemOrder


@admin.register(ItemOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("product", "cost")

    def cost(self, obj):
        cost = obj.price * obj.count
        return cost


@admin.register(Meson)
class MesonAdmin(admin.ModelAdmin):
    list_display = ("name", "show_product")

    def show_product(self, obj):
        product = obj.products.values_list("name", flat=True)
        print(list(product))
        return product[0:]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "color")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", )