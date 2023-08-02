from django.db import models


# Create your models here.
class BlogPost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    head0 = models.CharField(max_length=200)
    chead0 = models.CharField(max_length=2000)
    head1 = models.CharField(max_length=200)
    chead1 = models.CharField(max_length=2000)
    head2 = models.CharField(max_length=200)
    chead2 = models.CharField(max_length=2000)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="blog/images",default='')

    def __str__(self):
        return str(self.blog_id) + self.head0[:20]
