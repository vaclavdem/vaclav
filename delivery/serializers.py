from rest_framework import serializers

from .models import Restaurant, Food, Order, Report, CartProduct, Cart


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
        fields = ("food", "qty")


class OrderCreateSerializer(serializers.ModelSerializer):
    """Добавление заказа"""

    class Meta:
        model = Order
        exclude = ("status", "cart", "user", "final_price", "view_cart", "delivery", "is_active")


class OrderListSerializer(serializers.ModelSerializer):
    """Список заказов"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    view_cart = CartProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "name", "comment", "to", "view_cart", "final_price", "status")


class OrderUserListSerializer(serializers.ModelSerializer):
    """Список заказов для пользователя"""

    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    view_cart = CartProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ("comment", "to", "view_cart", "final_price", "status", "is_active")


class OrderEditSerializer(serializers.ModelSerializer):
    """Изменение статусат заказа"""

    class Meta:
        model = Order
        fields = ("status",)


class OrderDeliveredSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Order
        fields = ("is_deliveredd",)


class OrderTakeSerializer(serializers.ModelSerializer):
    """Принятие заказа"""

    class Meta:
        model = Order
        fields = ("is_active",)


class OrderEditUserSerializer(serializers.ModelSerializer):
    """Изменение заказа"""

    class Meta:
        model = Order
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
