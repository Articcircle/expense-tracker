from django.db import models

from django.contrib.auth.models import User
# Imports Django’s built-in User model
# Represents registered users (username, email, password, etc.)
# Used for authentication and authorization
# Create your models here.

class Expense(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category= models.CharField(max_length=50)
    date= models.DateField(auto_now_add=False)
    note=models.TextField(max_length=200,blank=True)

    def __str__(self):
        return self.category


# expense
# ------------------------
# id
# user_id
# amount
# category
# date
# note
