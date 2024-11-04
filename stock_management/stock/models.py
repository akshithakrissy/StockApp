from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Stock name
    quantity = models.PositiveIntegerField()              # Quantity available
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    # last_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    low_stock_threshold = models.PositiveIntegerField(default=10)

    def __str__(self):
        return str(self.name)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Order {self.order_id} - {self.stock.name}"
    
class Store(models.Model):
    store_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.store_name)

    
class StoreRequest(models.Model):
    # Define the fields for the StoreRequest model
    request_id = models.IntegerField() 
    item_name = models.CharField(max_length=100)     # Name of the item requested
    owner_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()           # Quantity requested
    requested_by = models.CharField(max_length=100)   # User who made the request
    request_date = models.DateTimeField(auto_now_add=True)  # Date when the request was made
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('denied', 'Denied'),
        ],
        default='pending'  # Default status of the request
    )

    def __str__(self):
        return f"Request ID: {self.request_id} - Item: {self.item_name} - Quantity: {self.quantity}"

    class Meta:
        verbose_name = "Store Request"
        verbose_name_plural = "Store Requests"
        ordering = ['-request_date']  # Order by request date (latest first)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=500, blank=True)

        
    def __str__(self):
        # pylint: disable=no-member
        return self.user.username