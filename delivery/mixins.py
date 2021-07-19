from rest_framework.views import APIView

from .models import (
    Users,
    Cart,
)


class CartMixin(APIView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = Users.objects.filter(user=request.user).first()
            if not user:
                user = Users.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                order = Cart.objects.create(user=user)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)
