from django.urls import path
from .views import (SignUpView, LoginView, LogoutView,
    CategoryViewSet,
    ItemViewSet,
    HallViewSet,
    TableViewSet,
    BookingViewSet,
    OrderViewSet,
    ProfileView,
    AnalyticsView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

category_list = CategoryViewSet.as_view({'get': 'list', 'post': 'create'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

item_list = ItemViewSet.as_view({'get': 'list', 'post': 'create'})
item_detail = ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

hall_list = HallViewSet.as_view({'get': 'list', 'post': 'create'})
hall_detail = HallViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

table_list = TableViewSet.as_view({'get': 'list', 'post': 'create'})
table_detail = TableViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

booking_list = BookingViewSet.as_view({'get': 'list', 'post': 'create'})
booking_detail = BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

order_list = OrderViewSet.as_view({'get': 'list', 'post': 'create'})
order_detail = OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    
      # Category
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),

    # Item
    path('items/', item_list, name='item-list'),
    path('items/<int:pk>/', item_detail, name='item-detail'),

    # Hall
    path('halls/', hall_list, name='hall-list'),
    path('halls/<int:pk>/', hall_detail, name='hall-detail'),

    # Table
    path('tables/', table_list, name='table-list'),
    path('tables/<int:pk>/', table_detail, name='table-detail'),
    
    # Booking
    path('bookings/', booking_list, name='booking-list'),
    path('bookings/<int:pk>/', booking_detail, name='booking-detail'),
    
    # Order
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]