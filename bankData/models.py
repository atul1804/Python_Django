from django.db import models

class Bank(models.Model):
    accountno = models.IntegerField(max_length=40)
    name = models.CharField(max_length=40)
    balance = models.IntegerField(max_length=40)

class signUP(models.Model):
    username = models.CharField(max_length=40)
    phoneNo = models.CharField(max_length=40)
    emailid = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    User_type = models.CharField(max_length=40)

class transactions(models.Model):
    user_id = models.IntegerField()
    AccountNo = models.IntegerField()
    t_type = models.CharField(max_length=30) 
    amount = models.IntegerField()
    balance = models.IntegerField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)

class fd(models.Model):
    user_id = models.IntegerField()
    fd_amount = models.IntegerField()
    int_rate = models.IntegerField()
    time_period = models.IntegerField()
    mat_amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    maturity_date = models.DateTimeField()
        