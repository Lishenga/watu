from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Customers, Logs, Forex, Transactions, Countries
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
import urllib.request
import datetime
import json
import stripe
import requests
import phonenumbers
from lipisha import Lipisha


#STRIPE_SECRET_KEY = "sk_test_hQcwVNlTH1MDVLggM1avFWr4"
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
LIPISHA_API_KEY = "7dcc707178043be384ad6d454f76698f"
LIPISHA_API_SIGNATURE = "ih5fBHxDmt5W5gQnGJWuMdpeNaCE1gOGCyazXVQxR+biVahPwlur7bCjjr3OvqlLCXPKq4z7BE1/CbHBune7M2YQgVQAPEBMSyNnlNNYZM5RxJsF3GJbPNhH5KZM9AuMIocZHA/jrlZIqUYSp5oO4c/RKkAZ5UtNir7IHwerV0E="
AFRICAS_TALKING_KEY="fec5de06057e87752728a462bd20aa1f8a55cce6e74351ec198c909fe8213972"
AFRICAS_TALKING_KEY_SANDBOX="4aee78f5814175d3bc47cde14f4a1268292992ecf13955f696982c726575f60e"


def create_log(request, tags, description):
    log = Logs(name= "logs",tags="Users", description="User Created", created_at = datetime.date.today(), updated_at= datetime.date.today())
    log.save()
    return True

def create_transaction(_from, to, amount):
    transaction = Transactions(
        transaction_ref = random_string(), 
        Sender=_from, Receiver=to, 
        Amount= amount, 
        status=0,
        created_at = datetime.date.today(), 
        updated_at= datetime.date.today()
    )
    transaction.save()
    return transaction

def random_string():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set*8, 8))


def check_rate_exsistence(high, low):
    
    quote = high+':'+low
    forex = Forex.objects.filter(quote=quote)

    if forex.count() is 0:

        quote = low+':'+high
        forex = Forex.objects.filter(quote=quote)

        if forex.count() is 0:
            return {
                'data':{},
                'status_code':500,
                'message':'empty'
            }
        
        else:
            return {
                'message':'exists',
                'status_code':200,
                'data':{
                    'id':forex.id,
                    'high':forex.high,
                    'low':forex.high,
                    'buying':forex.buying,
                    'selling':forex.selling,
                    'created_at':forex.created_at,
                    'updated_at':forex.updated_at
                }
            }

    else:
        return {
            'message':'exists',
            'status_code':200,
            'data':{
                'id':forex.id,
                'high':forex.high,
                'low':forex.high,
                'buying':forex.buying,
                'selling':forex.selling,
                'created_at':forex.created_at,
                'updated_at':forex.updated_at
            }
        }


def convert_currency(_from, to, amount):  
    currency = check_rate_exsistence(_from, to)

    if currency['status_code'] is 200:

        if currency['high'] == _from:
            result = amount * int(currency['buying'])
            return result

        elif currency['low'] == _from:
            result = amount/int(currency['selling'])
            return result

    else:
        raise Exception('Oops! Rate Does Not Exist')


def send_money_to_receiver(number, amount, country):
    if country == 'KE':
        
        return {
            "data":{},
            "message":"success",
            "status_code":200
        }
    
    else:

        stripe.api_key = STRIPE_SECRET_KEY

        stripe.Payout.create(
            amount=400,
            currency="usd",
        )

        return {
            "data":{},
            "message":"success",
            "status_code":200
        }
    


def convert_numbers_to_international(number, country):
    x = phonenumbers.parse(number, country)
    y = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return y


def send_sms(number, text):
    username = "adams_okode"
    apikey  = AFRICAS_TALKING_KEY
    to      = number
    # And of course we want our recipients to know what we really do
    message = text
    # Create a new instance of our awesome gateway class
    gateway = AfricasTalkingGateway(username, apikey)
  
    results = gateway.sendMessage(to, message)
    data=[]
    for recipient in results:
        values={
               "number":recipient['number'],
               "status":recipient['status'],
               "messageId":recipient['messageId'],
               "cost":recipient['cost']   
        }
        data.append(values)

    return data   


def send_simple_message(message,email,subject,name):
    return send_mail(subject, 
        message, 
        'admin@simplux.com',
        [email], 
        fail_silently=False
    )



def create_stripe_customer(email): 
    customer=Customers.objects.get(email=email)

    if customer.stripe_id =="0":
        my_customer = stripe.Customer.create(email= email, api_key=STRIPE_SECRET_KEY)
        customer = Customers.objects.get(email=email)
        customer.stripe_id = my_customer['id']
        customer.save()
        success={
            "data":my_customer,
            "message":"success",
            "status_code":200
        } 

        return success 

    else:  
        success={ 
            "message":"customer already exists",
            "status_code":200
        } 

        return success  

