from store.models import Product, Category,Order, OrderItem, Payment, Cart, CartItem
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from myapp.models import Users


class ProductTest(TestCase):
    def setUp(self):
        # I create fake browser
        self.client = APIClient()
        # I create a normal user
        self.user = Users.objects.create_user(
            first_name = 'Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_loggedin_users(self):
        # I force it to log in, pretent to be logged in user
        self.client.force_authenticate(user=self.user)
        # I get the endpoint
        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200) # Check if the status_code is 200. means user is logged in and can see products

    def test_loggedout_users(self):
        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 403)

class AddCartTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Computers')
        self.user = Users.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )
        self.product=Product.objects.create(
            name='Laptop',
            description='This is a good laptop',
            price=1299.99,
            category=self.category,
            stock=3
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

    def test_loggedin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/store/add_cart/', 
            {'product_id':self.product.id, 'quantity':1}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_loggedout_user(self):
        response = self.client.post(
            '/store/add_cart/',
            {'product_id':self.product.id, 'quantity':1}
        )
        self.assertEqual(response.status_code,403)



class CheckOutTest(TestCase):
    def setUp(self):
        # Create a fake browser
        self.client = APIClient()
        # Create a user
        self.user = Users.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )
        # Create a category
        self.category=Category.objects.create(name='Computers')
        # Create a product
        self.product=Product.objects.create(
            name='Laptop',
            description='Amazing Laptop',
            price=1500.00,
            category=self.category,
            stock=2
        )
        # Create a cart
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item=CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
    def test_loggedin_user(self):
        self.client.force_authenticate(user=self.user)
        response=self.client.post('/store/checkout/', {'address': '123 Main St'})
        self.assertEqual(response.status_code, 201)

    def test_loggedout_ueser(self):
        response=self.client.post('/store/checkout/', {'address': '123 Main St'})
        self.assertEqual(response.status_code, 403)


class PaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )
        self.order=Order.objects.create(
            user=self.user,
            address='123 Main Street',
            total_price=1500.00,
            status=Order.StatusChoices.PENDING,
        )
        
        self.transactionID='IOAH@#T%S'
        self.payment=Payment.objects.create(
            order=self.order,
            amount=self.order.total_price,
            payment_method=Payment.PaymentMethods.PAYPAL,
            status=Payment.StatusChoices.PENDING,
            transaction_id=self.transactionID
        )

    def test_successful_payment(self):
        self.payment.status = Payment.StatusChoices.SUCCESSFUL
        self.payment.save()
        self.order.status = Order.StatusChoices.PAID
        self.order.save()   
        
        self.assertEqual(self.order.status, Order.StatusChoices.PAID)

    def test_failed_payment(self):
        self.payment.status = Payment.StatusChoices.FAILED
        self.payment.save()
        self.order.status=Order.StatusChoices.CANCELLED
        self.order.save()
        
        self.assertEqual(self.order.status, Order.StatusChoices.CANCELLED)

    def test_loggedin_user(self):
        self.client.force_authenticate(user=self.user)
        response=self.client.post('/store/payment/', {'order_id':1,'payment_method':'PayPal', 'status':"Pending"})
        self.assertEqual(response.status_code,400)
    
    def test_loggedout_user(self):
        response=self.client.post('/store/payment/', {'order_id':1, 'payment_method':'PayPal', 'status':"Pending"})
        self.assertEqual(response.status_code,403)
        
# Integration Test:
"""
Integration Test for checking if everything works together, it is unlike unit test in python which tests small parts of code 
in isolation. 

Integration Test is for making sure everybody is alright and works together.
"""
