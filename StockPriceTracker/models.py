from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Info(models.Model):
    gmail_address = models.EmailField(max_length=254)
    gmail_password = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info')

    def __str__(self):
        return '%s %s' % (self.gmail_address, self.user_agent)


class Stock(models.Model):
    nasdaq_symbol = models.CharField(max_length=10)
    set_price = models.FloatField(blank=False, default=0)
    current_price = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stocks')

    def __str__(self):
        return '%s %f %f %s' % (self.nasdaq_symbol, self.set_price, self.current_price, str(self.passed))


