from django.db import models

# Create your models here.
class Customers(models.Model):
    
    fname = models.CharField(max_length=255, default=None)
    lname = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None, unique= True)
    password = models.CharField(max_length=255, default=None)
    status = models.IntegerField(default=0)
    msisdn = models.CharField(max_length=255, default=None)
    country_code = models.CharField(max_length=255, default=None)
    stripe_id = models.CharField(max_length=255, default=None)
    card_brand = models.CharField(max_length=255, default=None)
    card_last_four = models.CharField(max_length=255, default=None)
    trial_end_at = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)
    ##_gJbWdPH4Psx #alana_ftp_user

class Cards(models.Model): 

    object_1 = models.CharField(max_length=255, default=None)
    address_city=  models.CharField(max_length=255, default=None)
    address_country=  models.CharField(max_length=255, default=None)
    address_line1=  models.CharField(max_length=255, default=None)
    address_line2=  models.CharField(max_length=255, default=None)
    address_line1_check=  models.CharField(max_length=255, default=None)
    address_state=  models.CharField(max_length=255, default=None)
    address_zip=  models.CharField(max_length=255, default=None)
    brand=  models.CharField(max_length=255, default=None)
    address_zip_check=  models.CharField(max_length=255, default=None)
    country=  models.CharField(max_length=255, default=None)
    customer=  models.CharField(max_length=255, default=None)
    cvc_check=  models.CharField(max_length=255, default=None)
    dynamic_last4=  models.CharField(max_length=255, default=None)
    exp_month=  models.CharField(max_length=255, default=None)
    exp_year=  models.CharField(max_length=255, default=None)
    fingerprint=  models.CharField(max_length=255, default=None)
    funding=  models.CharField(max_length=255, default=None)
    last4=  models.CharField(max_length=255, default=None)
    metadata=  models.CharField(max_length=255, default=None)
    name=  models.CharField(max_length=255, default=None)
    tokenization_method=  models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Clients(models.Model):

    client_id = models.CharField(max_length=255, default=None)
    access_level = models.CharField(max_length=255, default=None)
    client_secret = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)


class Transactions(models.Model):
    transaction_ref = models.CharField(max_length=255, default=None, unique=True)
    Amount = models.IntegerField(default=0)
    Sender = models.CharField(max_length=255, default=None)
    Receiver = models.CharField(max_length=255, default=None)
    currency = models.CharField(max_length=55, default=None)
    stripe_reference = models.CharField(max_length=255, default=None, blank=True, null=True)
    mpesa_code = models.CharField(max_length=255, default=None, blank=True, null=True)
    usd_amount = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Accounts(models.Model):
    name = models.CharField(max_length=255, default=None)
    owner = models.CharField(max_length=255, default=None)
    balance = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Logs(models.Model):

    description = models.CharField(max_length=255, default=None)
    tags = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Forex (models.Model):
    high = models.CharField(max_length=255, default=None) 
    low = models.CharField(max_length=255, default=None) 
    quote = models.CharField(max_length=255, default=None, unique = True) 
    amount = models.IntegerField(default=0)
    buying = models.IntegerField(default=0)
    selling = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Settings(models.Model):
    name = models.CharField(max_length=255, default=None) 
    value = models.IntegerField(default=0)

class Chats(models.Model):

    chat_id =   models.CharField(max_length=255, default=None)
    member_1 =  models.CharField(max_length=255, default=None)
    member_2 =  models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)
    
class Messages(models.Model):

    chat_id =   models.CharField(max_length=255, default=None)
    sender =  models.CharField(max_length=255, default=None)
    receiver =  models.CharField(max_length=255, default=None)
    message =  models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class SocketDetails(models.Model):

    msisdn = models.CharField(max_length=255, default=None, unique= True)
    player_id = models.CharField(max_length=255, default=None)

class Countries (models.Model):
    name = models.CharField(max_length=255, default=None, unique= True)
    country_code = models.CharField(max_length=50, default=None, unique= True)
    currency_code = models.CharField(max_length=50, default=None, unique= True)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class Tariffs (models.Model):
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=0)
    tariff_type = models.CharField(max_length=50, default=None, unique= True)
    amount = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)
