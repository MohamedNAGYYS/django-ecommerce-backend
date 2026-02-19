from django.shortcuts import get_object_or_404
from store.serializers import ProductSerializer, CartItemSerializer,OrderItemSerializer, PaymentSerializer, OrderSerializer
from store.backends import IsAdminUserRole
from store.models import Product, Order, OrderItem, Payment, Cart, CartItem
from rest_framework import viewsets, status
from rest_framework import generics,permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    # Only admins can create, update, destroy..
    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            return [IsAdminUserRole()] 
        return []
    

class AllProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['id','name','description']
    ordering_fields = ['name','price']
    

class OrderView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        order = Order.objects.filter(user=user)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AddCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        product= get_object_or_404(Product, id=product_id)


        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created=CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity':quantity}
        )
        quantity = int(request.data.get('quantity',1)) # Default is 1 if not provided
        
        # Check if user typed 0 or less in quantity
        if quantity <= 0:
            return Response({'error':"Quantity must be positive"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response({'message':"Product added to cart."}, status=status.HTTP_200_OK)



class DeleteFromCart(APIView):
    def post(self, request):
        product = request.data.get('product_id')
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product)
        item.delete()
        return Response({'message':"Product has been deleted from your cart."}, status=status.HTTP_200_OK)

class CartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    


class CheckOut(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error":"Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
    
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response({'message':f"Not enough stock {item.product.name}."}, status=status.HTTP_406_NOT_ACCEPTABLE)


        order=Order.objects.create(
            user=request.user,
            address=request.data.get('address',''),
            total_price=0,
            status=Order.StatusChoices.PENDING
        )

        total=0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            total += item.product.price * item.quantity

            item.product.stock -= item.quantity
            item.product.save()
        
        order.total_price = total
        order.save()
        cart_items.delete()
        return Response({'message': 'Order created successfully.', 'order_id': order.id}, status=status.HTTP_201_CREATED)





def transactionId(length=12):
    import random, string
    strings = list(string.ascii_letters + string.digits)
    # random.shuffle(strings)
    return ''.join(random.choice(strings) for _ in range(length))

class PaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    
    def post(self, request):
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        payment_method = request.data.get('payment_method')
        payment_status = request.data.get('status')

        if payment_method not in Payment.PaymentMethods.values:
            return Response({'error':'Invalid Payment method'}, status=status.HTTP_400_BAD_REQUEST)

        if payment_status not in Payment.StatusChoices.values:
            return Response({'error':'Invalid Payment status'}, status=status.HTTP_400_BAD_REQUEST)


        payment = Payment.objects.create(
            order=order, 
            amount=order.total_price,
            payment_method=payment_method, 
            status=payment_status,
            transaction_id=transactionId()
        )


        if payment_status == 'Successful':
            order.status = Order.StatusChoices.PAID
            order.save()
            payment.save()
            return Response({'message':"Order paid successfully.", 'payment_method':payment_method}, status=status.HTTP_202_ACCEPTED)
        
        elif payment_status == 'Failed':
            order.status = Order.StatusChoices.CANCELLED
            order.save()
            return Response({'message':"Payment failed."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message":"Invalid payment status."}, status=status.HTTP_400_BAD_REQUEST)
    
