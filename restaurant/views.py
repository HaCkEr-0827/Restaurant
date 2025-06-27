from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import CustomUser, Category, Item, Hall, Table, Booking, Order, OrderItem
from .serializers import UserSerializer, CategorySerializer, ItemSerializer, HallSerializer, TableSerializer, BookingSerializer, OrderSerializer, OrderItemSerializer, OrderCreateItemSerializer, OrderCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import logout
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAdminRole
from datetime import time as dtime, datetime
from django.db.models import Count
from .models import OTPCode
from .utils import generate_otp, save_otp_to_cache


class SignUpView(APIView):
    @swagger_auto_schema(
        operation_description="Telefon raqamga OTP kod yuborish.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone_number"],
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='+998901234567',
                    description='Foydalanuvchi telefon raqami'
                ),
            },
        ),
        responses={
            200: openapi.Response(description='OTP yuborildi'),
            400: openapi.Response(description='Xatolik: telefon raqami yuborilmagan yoki noto‘g‘ri')
        }
    )
    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({'error': 'Telefon raqami majburiy'}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_otp()  # Masalan, 6 xonali random kod
        OTPCode.objects.create(phone_number=phone, code=otp_code)

        print(f"📲 OTP kod: {otp_code} → {phone}")  # Aslida SMS orqali yuboriladi

        return Response({'message': 'OTP yuborildi'}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    @swagger_auto_schema(
        operation_description="OTP kodni tasdiqlab foydalanuvchini ro'yxatdan o'tkazish.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone_number', 'otp', 'name', 'password'],
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, example="123456"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, example="Ali Valiyev"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', example="MySecret123"),
            },
        ),
        responses={
            201: openapi.Response('Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi'),
            400: openapi.Response('Xatolik: OTP noto‘g‘ri yoki muddati o‘tgan, yoki foydalanuvchi allaqachon mavjud')
        }
    )
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('otp')
        name = request.data.get('name')
        password = request.data.get('password')

        otp_obj = OTPCode.objects.filter(phone_number=phone, code=code, is_used=False).last()

        if not otp_obj or otp_obj.is_expired():
            return Response({'error': 'OTP is invalid or expired'}, status=400)

        if CustomUser.objects.filter(phone_number=phone).exists():
            return Response({'error': 'User already exists'}, status=400)

        user = CustomUser.objects.create(phone_number=phone, name=name)
        user.set_password(password)
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return Response({'message': 'User registered successfully'}, status=201)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Foydalanuvchini telefon raqami va paroli orqali tizimga kiritadi. Muvaffaqiyatli login bo‘lsa, access va refresh token qaytariladi.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example="your_password"),
            },
            required=['phone_number', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "access": "your_access_token",
                        "refresh": "your_refresh_token"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "error": "Invalid credentials"
                    }
                }
            )
        }
    )
    def post(self, request):
        phone = request.data.get('phone_number')
        password = request.data.get('password')

        user = CustomUser.objects.filter(phone_number=phone).first()
        if user and user.check_password(password):
            access = str(AccessToken.for_user(user))
            refresh = str(RefreshToken.for_user(user))
            return Response({
                'message': 'Login successful',
                'access': access,
                'refresh': refresh
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

class ForgotPasswordRequestOTPView(APIView):
    @swagger_auto_schema(
        operation_summary="Parolni tiklash uchun OTP yuborish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
            },
            required=['phone_number']
        ),
        responses={
            200: openapi.Response(description="OTP yuborildi"),
            404: openapi.Response(description="Foydalanuvchi topilmadi")
        }
    )
    def post(self, request):
        phone = request.data.get('phone_number')
        user = CustomUser.objects.filter(phone_number=phone).first()

        if not user:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

        otp = generate_otp()
        save_otp_to_cache(phone, otp)

        print(f"🔐 OTP for password reset: {otp}")

        return Response({"message": "OTP yuborildi"}, status=200)
    
class ForgotPasswordVerifyOTPAndSetNewPasswordView(APIView):
    
    @swagger_auto_schema(
        operation_summary="OTP orqali parolni yangilash",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, example="1234"),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, example="newsecurepassword"),
            },
            required=['phone_number', 'otp', 'new_password']
        ),
        responses={
            200: openapi.Response(description="Parol muvaffaqiyatli yangilandi"),
            400: openapi.Response(description="OTP noto‘g‘ri yoki vaqt tugagan")
        }
    )
    def post(self, request):
        phone = request.data.get('phone_number')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        user = CustomUser.objects.filter(phone_number=phone).first()
        if not user:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

        from .utils import verify_otp_from_cache
        if not verify_otp_from_cache(phone, otp):
            return Response({"error": "OTP noto‘g‘ri yoki vaqt tugagan"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Parol muvaffaqiyatli yangilandi"}, status=200)


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Login bo‘lgan foydalanuvchi parolni yangilaydi",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['old_password', 'new_password']
        ),
        responses={
            200: openapi.Response(description="Parol yangilandi"),
            400: openapi.Response(description="Eski parol noto‘g‘ri")
        }
    )
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Eski parol noto‘g‘ri"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Parol yangilandi"}, status=200)


class CategoryViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticatedOrReadOnly()]
    
    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: CategorySerializer()})
    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer, responses={201: CategorySerializer()})
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=CategorySerializer, responses={200: CategorySerializer()})
    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)
    
    
class ItemViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticatedOrReadOnly()]
    
    @swagger_auto_schema(responses={200: ItemSerializer(many=True)})
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ItemSerializer()})
    def retrieve(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ItemSerializer, responses={201: ItemSerializer()})
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=ItemSerializer, responses={200: ItemSerializer()})
    def update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=204)
    
class HallViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticatedOrReadOnly()]

    @swagger_auto_schema(responses={200: HallSerializer(many=True)})
    def list(self, request):
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: HallSerializer()})
    def retrieve(self, request, pk=None):
        hall = get_object_or_404(Hall, pk=pk)
        serializer = HallSerializer(hall)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=HallSerializer, responses={201: HallSerializer()})
    def create(self, request):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=HallSerializer, responses={200: HallSerializer()})
    def update(self, request, pk=None):
        hall = get_object_or_404(Hall, pk=pk)
        serializer = HallSerializer(hall, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        hall = get_object_or_404(Hall, pk=pk)
        hall.delete()
        return Response(status=204)

    

class TableViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticatedOrReadOnly()]

    @swagger_auto_schema(responses={200: TableSerializer(many=True)})
    def list(self, request):
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: TableSerializer()})
    def retrieve(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TableSerializer, responses={201: TableSerializer()})
    def create(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=TableSerializer, responses={200: TableSerializer()})
    def update(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        table = get_object_or_404(Table, pk=pk)
        table.delete()
        return Response(status=204)
    
    

class BookingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: BookingSerializer(many=True)})
    def list(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: BookingSerializer()})
    def retrieve(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={201: BookingSerializer()}
    )
    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            table = serializer.validated_data['table']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']

            # Ish vaqti tekshiruvi
            if not (dtime(10, 0) <= time <= dtime(23, 0)):
                return Response(
                    {'error': 'Ish vaqti 10:00–23:00 oralig‘ida bo‘lishi kerak.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Bandlik tekshiruvi
            already_booked = Booking.objects.filter(
                table=table, date=date, time=time, status='approved'
            ).exists()
            if already_booked:
                return Response(
                    {'error': 'Bu stol allaqachon band qilingan.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={200: BookingSerializer()}
    )
    def update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: OrderSerializer()})
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=OrderCreateSerializer,
        responses={201: OrderSerializer()}
    )
    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=["pending", "approved", "rejected"])
            },
            required=["status"]
        ),
        responses={200: OrderSerializer()}
    )
    def update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        status_value = request.data.get("status")
        if status_value not in ["pending", "approved", "rejected"]:
            return Response({"error": "Noto‘g‘ri status"}, status=400)
        order.status = status_value
        order.save()
        print(f"📩 Bildirishnoma: Buyurtma holati o‘zgardi → {order.status}")
        return Response(OrderSerializer(order).data)

    @swagger_auto_schema(responses={204: 'Deleted'})
    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        top_items = OrderItem.objects.values('item__name').annotate(
            total=Count('id')
        ).order_by('-total')[:5]
        return Response(top_items)