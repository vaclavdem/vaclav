from rest_framework import serializers

from .models import (
    Restaurant,
    Food,
    Order,
    Report,
    CartProduct,
    Small_order,
)


class RestaurantListSerializer(serializers.ModelSerializer):
    """Список ресторанов"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Restaurant
        fields = ("title", "cooking_time", "min_price", "category")


class FoodSerializer(serializers.ModelSerializer):
    """Еда"""

    class Meta:
        model = Food
        fields = ("name", "description", "type_discount", "price", "percent", "discounted_price", "restaurant")


class FoodCreateChangeSerializer(serializers.ModelSerializer):
    """Создание и изменение еды"""

    class Meta:
        model = Food
        fields = ("name", "description", "type_discount", "price", "percent")


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ("food", "qty", "final_price")


class OrderCreateSerializer(serializers.ModelSerializer):
    """Добавление заказа"""

    class Meta:
        model = Order
        fields = ("email", "name", "to", "comment")


class OrderListSerializer(serializers.ModelSerializer):
    """Список заказов"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    restaurant = serializers.SlugRelatedField(slug_field="title", read_only=True)
    cart_product = CartProductSerializer(many=True)

    class Meta:
        model = Small_order
        fields = ("id", "name", "comment", "fromm", "to", "cart_product", "final_price", "status", "restaurant")


class OrderProductUserListSerializer(serializers.ModelSerializer):
    """Подробная информация по маленькому заказу"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    restaurant = serializers.SlugRelatedField(slug_field="title", read_only=True)
    cart_product = CartProductSerializer(many=True)

    class Meta:
        model = Small_order
        fields = ("cart_product", "final_price", "status", "is_active", "is_delivered", "restaurant")


class OrderUserListSerializer(serializers.ModelSerializer):
    """Список заказов для пользователя"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    small_order = OrderProductUserListSerializer(many=True)

    class Meta:
        model = Order
        fields = ("comment", "to", "small_order", "final_price", "status")


class OrderEditSerializer(serializers.ModelSerializer):
    """Изменение статусат заказа"""

    class Meta:
        model = Small_order
        fields = ("status",)


class OrderDeliveredSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Small_order
        fields = ("is_delivered",)


class OrderTakeSerializer(serializers.ModelSerializer):
    """Принятие заказа"""

    class Meta:
        model = Small_order
        fields = ("is_active",)


class OrderEditUserSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Small_order
        fields = ("comment", "to",)


class ReportSerializer(serializers.ModelSerializer):
    """Жалоба"""

    class Meta:
        model = Report
        fields = ("email", "order", "comment", "id")


class ReportUserSerializer(serializers.ModelSerializer):
    """Добавление жалобы"""

    class Meta:
        model = Report
        fields = ("email", "comment")


class AddToCartSerializer(serializers.ModelSerializer):
    """обавление товара в корзину"""

    class Meta:
        model = CartProduct
        fields = ("qty",)


class CartSerializer(serializers.ModelSerializer):
    """Корзина"""

    class Meta:
        model = CartProduct
        fields = ("qty", "food_id", "final_price")
