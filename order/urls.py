from django.urls import path
from .views import Index, SignUp, Login, Logout, Cart, CheckOut, OrderView, Profile, Updateprofile, UpdatePassword, delete_order, remove_from_cart, Payment

urlpatterns = [
    path('',Index.as_view(), name='homepage'),
    path('signup', SignUp.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', CheckOut.as_view(), name='checkout'),
    path('payment', Payment.as_view(), name='payment'),
    path('orders', OrderView.as_view(), name='orders'),
    path('profile',Profile.as_view(), name='profile'),
    path('updateprofile', Updateprofile.as_view(), name='updateprofile'),
    path('update-password', UpdatePassword.as_view(), name='update-password'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
