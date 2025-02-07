from django.db import models
from Admin_App.models import Item
from django.contrib.auth.models import User

class Viewers(models.Model):
    username=models.CharField(max_length=30,default='default_username')
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=20)


class Cart(models.Model):
    user = models.ForeignKey(Viewers, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def total_price(self):
        return int(self.product.item_price.replace(',','')) * self.quantity
    

class BuyNow(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    ]
    
    COLOR_CHOICES = [
        ("Red", "Red"),
        ("Blue", "Blue"),
        ("Green", "Green"),
        ("Black", "Black"),
        ("White", "White"),
    ]

    user = models.ForeignKey(Viewers, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="M")  # Default size: Medium
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="Black")  
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user} - {self.product} ({self.payment_status})"

class review(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name='comment_set')
    user=models.ForeignKey(Viewers,on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    

class DeliveryAddress(models.Model):

    user = models.ForeignKey(Viewers, on_delete=models.CASCADE)  
    orders = models.ForeignKey(BuyNow,on_delete=models.CASCADE,default=1)
    phone_number = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default='India')

    def __str__(self):
        return f"{self.full_name}, {self.city}"




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('PAYPAL', 'PayPal'),
        ('COD', 'Cash on Delivery'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    user = models.ForeignKey(Viewers, on_delete=models.CASCADE, related_name='payments')
    orders = models.ForeignKey(BuyNow, on_delete=models.CASCADE,default=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} for {self.product.item_name} on {self.date_time}"












































    











    


    





    
    