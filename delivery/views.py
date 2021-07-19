from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .mixins import CartMixin
from .utils import recalc_cart
import time
from datetime import datetime
from django.shortcuts import redirect

from .tasks import (
    send_order_email,
    send_report_email,
    send_change_status_email,
    send_take_email,
    send_delivered_email,
)

from .models import (
    Restaurant,
    Food,
    Order,
    Report,
    CartProduct,
    Users,
    Cart,
)

from .serializers import (
    RestaurantListSerializer,
    FoodSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
    OrderEditSerializer,
    ReportSerializer,
    ReportUserSerializer,
    AddToCartSerializer,
    CartSerializer,
    OrderUserListSerializer,
    OrderEditUserSerializer,
    OrderTakeSerializer,
    FoodCreateChangeSerializer,
    OrderDeliveredSerializer,
)

from .permissions import (
    IsDeliveryUser,
    IsRestaurantUser,
    IsModeratorUser,
)


class RestaurantListView(generics.ListAPIView):
    """Вывод списка ресторанов"""
    serializer_class = RestaurantListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Restaurant.objects.filter(draft=False)


class FoodListView(APIView):
    """Вывод списка еды"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        queryset = Food.objects.filter(restaurant=pk)
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderListView(generics.ListAPIView):
    """Просмотр заказов доставщиками"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(is_active=False)
        return queryset


class OrderEditView(generics.RetrieveUpdateAPIView):
    """Изменение статуса заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderEditSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Order.objects.filter(is_active=True, delivery=user)
        order = Order.objects.get(id=self.kwargs.get('pk'))
        send_change_status_email(order.email)
        return queryset


class OrderCreateView(generics.CreateAPIView):
    """Создание заказа"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        serializer.save(user=user, cart=cart, view_cart=cart.food.all(), final_price=cart.final_price)
        cart.food.clear()
        cart.final_price = 0
        cart.save()
        send_order_email(self.request.data.get("email"))


class OrderTakeView(generics.RetrieveUpdateAPIView):
    """Взятие заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderTakeSerializer
    queryset = Order.objects.filter(is_active=False)

    def put(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        send_take_email(order.email)
        user = Users.objects.get(user=self.request.user)
        order.delivery = user
        order.is_active = True
        order.save()
        return Response(request.data)


class OrderDeliveredView(generics.RetrieveUpdateAPIView):
    """Изменение основного статуса заказа"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderDeliveredSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Order.objects.filter(is_active=True, delivery=user)
        return queryset

    def put(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        send_delivered_email(order.email)
        order.is_deliveredd = True
        order.ddelivered_at = time.mktime(datetime.now().timetuple())
        order.save()
        return Response(request.data)


class OrderTakenView(generics.ListAPIView):
    """просмотр взятых заказов"""
    permission_classes = (IsDeliveryUser,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        queryset = Order.objects.filter(delivery=user, is_active=True)
        return queryset


class OrderListUserView(generics.ListAPIView):
    """просмотр заказов клиентами"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderUserListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset


class OrderDeleteUserView(generics.RetrieveDestroyAPIView):
    """Удаление заказа клиентом"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderUserListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset


class OrderChangeUserView(generics.RetrieveUpdateAPIView):
    """Редактирование заказа клиентом"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderEditUserSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id)
        return queryset


class FoodCreateView(generics.CreateAPIView):
    """Добавление еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodCreateChangeSerializer

    def perform_create(self, serializer):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        serializer.save(restaurant=restaurant)


class FoodEditUserView(generics.RetrieveUpdateAPIView):
    """Редактирование еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodCreateChangeSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        queryset = Food.objects.filter(restaurant=restaurant)
        return queryset


class FoodDeleteUserView(generics.RetrieveDestroyAPIView):
    """Удаление еды"""
    permission_classes = (IsRestaurantUser,)
    serializer_class = FoodSerializer

    def get_queryset(self):
        user = Users.objects.get(user=self.request.user)
        restaurant = Restaurant.objects.get(restaurant_owner=user)
        queryset = Food.objects.filter(restaurant=restaurant)
        return queryset


class ReportsView(generics.ListAPIView):
    """Вывод списка ресторанов"""
    serializer_class = ReportSerializer
    permission_classes = (IsModeratorUser,)
    queryset = Report.objects.all()


class ReportDestroyView(generics.RetrieveDestroyAPIView):
    """Удаление жалобы"""
    permission_classes = (IsModeratorUser,)
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportCreateView(generics.CreateAPIView):
    """Добавление жалоб"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportUserSerializer

    def perform_create(self, serializer):
        order = Order.objects.get(id=self.kwargs.get('pk'))
        now = time.mktime(datetime.now().timetuple())
        if now - order.ddelivered_at < 300:
            serializer.save(order=order)
            send_report_email(self.request.data.get("email"))
        else:
            pass


class AddFoodToCartView(CartMixin, generics.CreateAPIView):
    """Добавление продукта в корзину"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddToCartSerializer

    def perform_create(self, serializer):
        food = Food.objects.get(id=self.kwargs.get('pk'))
        serializer.save(user_id=self.request.user.id, food=food)
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        product = CartProduct.objects.filter(user_id=self.request.user.id, food_id=self.kwargs.get('pk'),
                                             qty=self.request.data.get("qty")).last()
        cart.food.add(product)
        recalc_cart(cart)


class CartView(APIView):
    """Корзина"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = CartProduct.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)


class CartProductDestroyView(generics.RetrieveDestroyAPIView):
    """Удаление продукта из корзины"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = CartProduct.objects.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        user = Users.objects.get(user=self.request.user)
        cart = Cart.objects.get(user=user)
        recalc_cart(cart)
