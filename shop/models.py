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