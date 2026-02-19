from rest_framework import serializers
from store.models import Product, Payment, Order, OrderItem, Cart, CartItem, Category
from myapp.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','first_name', 'last_name','email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), write_only=True)
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price','category', 'category_id','stock']

class CartSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    user_id=serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(),source='user',write_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','user_id']


class CartItemSerializer(serializers.ModelSerializer):
    cart=CartSerializer(read_only=True)
    cart_id=serializers.PrimaryKeyRelatedField(source='cart',queryset=Cart.objects.all(), write_only=True)

    product=ProductSerializer(read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(source='product',queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ['id','cart','cart_id','product','product_id','quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    user_id=serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(),source='user',write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'address','total_price','status','created_at','updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    order=OrderSerializer(read_only=True)
    order_id=serializers.PrimaryKeyRelatedField(write_only=True,source='order',queryset=Order.objects.all())
    product=ProductSerializer(read_only=True)
    product_id=serializers.PrimaryKeyRelatedField(write_only=True,source='product',queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order','order_id','product','product_id','quantity','price']


class PaymentSerializer(serializers.ModelSerializer):
    order=OrderSerializer(read_only=True)
    order_id=serializers.PrimaryKeyRelatedField(write_only=True,source='order',queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = ['id','order','order_id','amount','status','payment_method','transaction_id','created_at']