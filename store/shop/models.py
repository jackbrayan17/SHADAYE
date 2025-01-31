from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('courier', 'Courier'),
        ('storekeeper', 'Storekeeper'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")

    def __str__(self):
        return self.username
# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Added stock tracking
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

# Order Model
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'), 
            ('Confirmed', 'Confirmed'), 
            ('Delivered', 'Delivered'), 
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'), 
            ('Paid', 'Paid'), 
            ('Failed', 'Failed')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# Testimonials Model
class Testimonial(models.Model):
    customer = models.CharField(max_length=255)  # Make sure this exists
    comment = models.TextField()  # Instead of content, if necessary
    rating = models.IntegerField()
    image = models.ImageField(upload_to="testimonials/")
    approved = models.BooleanField(default=False)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return f"{self.customer} - {self.rating} stars"
