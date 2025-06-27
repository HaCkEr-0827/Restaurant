from rest_framework import serializers
from .models import (
    CustomUser, Category, Item, Hall, Table,
    Booking, Order, OrderItem
)

# 🔹 1. CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'name', 'created_at']


# 🔹 2. Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# 🔹 3. Item (read uchun category nomi bilan)
class ItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = '__all__'


# 🔹 4. Hall
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


# 🔹 5. Table
class TableSerializer(serializers.ModelSerializer):
    hall = serializers.StringRelatedField()

    class Meta:
        model = Table
        fields = '__all__'


# 🔹 6. Booking
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

# 🔹 7. OrderItem (read)
class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    table = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'item_name', 'quantity', 'table']

    def get_table(self, obj):
        if obj.order and obj.order.table:
            return {
                'id': obj.order.table.id,
                'number': obj.order.table.number,
                'hall': obj.order.table.hall.name
            }
        return None
    
# 🔹 8. Order (read)
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    table = serializers.StringRelatedField()
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'table', 'status', 'created_at', 'items']


# 🔹 9. OrderItem (create uchun ichki serializer)
class OrderCreateItemSerializer(serializers.Serializer):
    item = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


# 🔹 10. Order (POST uchun)
class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderCreateItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['table', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                item_id=item_data['item'],
                quantity=item_data['quantity']
            )
        return order
