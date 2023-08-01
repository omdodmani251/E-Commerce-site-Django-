from django.db import models


# Create your models here.
class Product(models.Model):
    prod_id = models.AutoField
    prod_name = models.CharField(max_length=30)
    prod_desc = models.CharField(max_length=300)
    category = models.CharField(max_length=20,default="")
    subcategory = models.CharField(max_length=20,default="")
    price = models.IntegerField(default=0)
    prod_pub = models.DateField()
    image = models.ImageField(upload_to='shop/images',default="")

    def __str__(self):
        return self.prod_name

class Feedback(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    desc = models.CharField(max_length=300)
   

    def __str__(self):
        return self.name

class Order(models.Model):
    ord_id=models.AutoField(primary_key=True)
    items_info=models.CharField(max_length=5000)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    address1=models.CharField(max_length=100,default='')
    address2=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zip_code=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)


class Order_tracker(models.Model):
    track_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField()
    track_desc=models.CharField(max_length=100)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)+" "+self.track_desc[:12]