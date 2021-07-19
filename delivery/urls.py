from django.urls import path

from . import views

urlpatterns = [
    path("restaurants/", views.RestaurantListView.as_view()),
    path("restaurants/<int:pk>/", views.FoodListView.as_view()),
    path("order/create/", views.OrderCreateView.as_view()),
    path("order/user/", views.OrderListUserView.as_view()),
    path("order/delivery/", views.OrderListView.as_view()),
    path("order/delivery/taken/", views.OrderTakenView.as_view()),
    path("order/delivery/<int:pk>/", views.OrderEditView.as_view()),
    path("order/delivery/<int:pk>/take/", views.OrderTakeView.as_view()),
    path("order/delivery/<int:pk>/complete/", views.OrderDeliveredView.as_view()),
    path("order/user/<int:pk>/delete/", views.OrderDeleteUserView.as_view()),
    path("order/user/<int:pk>/change/", views.OrderChangeUserView.as_view()),
    path("addfood/", views.FoodCreateView.as_view()),
    path("food/<int:pk>/change/", views.FoodEditUserView.as_view()),
    path("food/<int:pk>/delete/", views.FoodDeleteUserView.as_view()),
    path("reports/", views.ReportsView.as_view()),
    path("reports/<int:pk>/create/", views.ReportCreateView.as_view()),
    path("reports/<int:pk>/delete/", views.ReportDestroyView.as_view()),
    path("foodaddtocart/<int:pk>/", views.AddFoodToCartView.as_view()),
    path("cart/", views.CartView.as_view()),
    path("cart/<int:pk>/delete/", views.CartProductDestroyView.as_view()),
]
