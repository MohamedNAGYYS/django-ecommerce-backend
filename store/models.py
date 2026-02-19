from django.db import models
from myapp.models import Users


# Category
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
# Products
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=10)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    def __str__(self):
        return self.name

# Cart
class Cart(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)

# Cart Item
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price
    

# Orders
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING='Pending'
        PAID='Paid'
        DELIVERED='Delivered'
        CANCELLED='Cancelled'
        SHIPPED='Shipped'
    
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    address=models.TextField(blank=True)
    total_price=models.DecimalField(decimal_places=2,max_digits=10)
    status=models.CharField(max_length=30,choices=StatusChoices.choices,default=StatusChoices.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Order #{self.id}'

# OrderItem
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"Order Item #{self.id}"

# Payments
class Payment(models.Model):
    class PaymentMethods(models.TextChoices):
        PAYPAL='PayPal'
        CREDIT='Credit Card'
        STRIPE='Stripe'
        
    class StatusChoices(models.TextChoices):
        PENDING='Pending'
        SUCCESSFUL='Successful'
        FAILED='Failed'
    
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_method=models.CharField(max_length=50,choices=PaymentMethods.choices)
    status=models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.PENDING)
    transaction_id=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.payment_method}"