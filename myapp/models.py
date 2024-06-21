from django.db import models
from django.utils.safestring import mark_safe



sta = [
    ('0','ACTIVE'),
    ('1','INACTIVE')
]
# Create your models here.
class registration(models.Model):
    name = models.CharField(max_length=40)
    dp = models.ImageField(upload_to='photos')
    gender = models.CharField(max_length=6)
    email = models.EmailField()
    phone_no = models.BigIntegerField()
    dob = models.DateField()
    address = models.TextField()
    r_type = models.CharField(max_length=10,null=True)
    password = models.CharField(max_length=8)
    r_status = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def dp_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.dp.url))

    dp_photo.allow_tags = True


class services(models.Model):
    sname = models.CharField(max_length=40)
    sprice = models.IntegerField()
    sdesc = models.TextField()
    simg = models.ImageField(upload_to='photos')
    email_id = models.ForeignKey(registration,on_delete=models.CASCADE)
    s_status = models.IntegerField(null=True)

    def sphoto(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.simg.url))

    sphoto.allow_tags = True

    def __str__(self):
        return self.sname


class booking(models.Model):
    userid = models.ForeignKey(registration, on_delete=models.CASCADE)
    serviceid = models.ForeignKey(services, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True)
    address = models.TextField()
    contact = models.IntegerField()
    b_status = models.IntegerField()
    pay_type = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.userid.name if self.userid else None

class contactus(models.Model):
    name = models.CharField(max_length=50)
    uemail = models.EmailField()
    phone = models.BigIntegerField()
    subject = models.CharField(max_length=30)
    message = models.TextField()

class feedback(models.Model):
    book_id = models.ForeignKey(booking,on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_time= models.DateTimeField(auto_now_add=True)