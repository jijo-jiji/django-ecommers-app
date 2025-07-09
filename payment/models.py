from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    
    user =models.ForeignKey(User,on_delete=models.CASCADE, null = True,blank=True)
    shipping_fullname = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255,null=True,blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255,null=True,blank=True)
    shipping_zipcode = models.CharField(max_length=255,null=True,blank=True)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Shipping Address"
    def __str__(self):
        return f'shipping address -{str(self.id)}'
    
    def create_shipping(sender, instance, created, **kwargs):
        if created:
            ShippingAddress.objects.create(
                user=instance,
                full_name=instance.get_full_name(), # Gets the user's name
                email=instance.email, # Gets the user's email
            )

    # Connect the signal
    post_save.connect(create_shipping, sender=User)
    
class Order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE, null = True,blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=150000)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped =models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True,null=True)
    
  # models.py

    def __str__(self):
        # ✅ CORRECT: Access the id attribute directly
        return f'Order - {self.id}'
    
    
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
    if instance.pk:
        now =datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null = True)
    product =models.ForeignKey(Product,on_delete=models.CASCADE, null = True)
    user =models.ForeignKey(User,on_delete=models.CASCADE, null = True,blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price =models.DecimalField(max_digits=7,decimal_places=2)
    
# models.py

    def __str__(self):
        # ✅ CORRECT: Access the id attribute directly
        return f'Order item - {self.id}'
    
