from django.db import models

# Create your models here.
class user(models.Model):
    first_name=models.CharField(max_length=20,null=True,blank=True )
    last_name=models.CharField(max_length=20,null=True,blank=True )
    age=models.IntegerField(null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    addhar_number=models.IntegerField(null=True,blank=True)
    pan_number=models.CharField(max_length=20,null=True,blank=True)
    password=models.CharField(max_length=20,null=True,blank=True)
    confirm_password=models.CharField(max_length=20,null=True,blank=True)
    account_type=models.CharField(max_length=20,null=True,blank=True)

    account_number=models.IntegerField(null=True,blank=True)
    account_balance=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.first_name
    
class card_details(models.Model):
    customer=models.ForeignKey(user,on_delete=models.CASCADE)
    card_number=models.CharField(max_length=10,blank=True ,null=True)
    cvv_number=models.IntegerField(null=True,blank=True)
    expiry_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.customer.first_name
    

class account_status(models.Model):
    account_holder=models.ForeignKey(user,on_delete=models.CASCADE)
    total_balance=models.FloatField(null=True,blank=True)
    current_balance=models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.account_holder.first_name

class reccuring_account_status(models.Model):
    holder=models.ForeignKey(user,on_delete=models.CASCADE)
    payment_date=models.DateField(null=True,blank=True)
    ammount=models.FloatField(default=0)
    
    def __str__(self):
        return self.holder.first_name


    