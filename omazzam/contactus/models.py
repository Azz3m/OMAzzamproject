from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contactus(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    areacode = models.IntegerField()
    telnum = models.IntegerField()
    email = models.EmailField()
    body = models.TextField()
    pub_date = models.DateTimeField()
    contact = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.firstname
    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime("%b %e %Y")
