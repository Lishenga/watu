from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Customers
from . import Logging
import stripe
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
from passlib.hash import django_pbkdf2_sha256 as password_handler
import datetime
from django.conf import settings



STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY


#STRIPE_SECRET_KEY = "sk_test_hQcwVNlTH1MDVLggM1avFWr4"
#create a new customer
@api_view(['POST'])
def create_customer(request):
    """
    Create Customer
    -----
        {
           
            fname:bavon,
            lname:Okode,
            email:aokode@yahoo.com,
            msisdn:254682312,
            password:Kurosaki8,
            country_code:KE
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            customer = Customers(
                fname=request.data['fname'],
                lname=request.data['lname'], 
                email=request.data['email'],  
                password=make_password(request.data['password']), 
                status='1', 
                msisdn=Logging.convert_numbers_to_international(request.data['msisdn'], request.data['country_code']),
                stripe_id='0' ,card_brand='0', 
                card_last_four='0',  
                trial_end_at='0',
                created_at = datetime.date.today(),
                updated_at= datetime.date.today()
            )
            customer.save()
            Logging.create_stripe_customer(request.data['email'])
            #Logging.send_sms(Logging.convert_numbers_to_international(request.data['msisdn'], request.data['country_code']))
            log=Logging.create_log(request= request, tags="Users", description="User Created")
            success={
                'message':'success',
                'log':log,
                'status_code':200
            }
            message='Your Account Has Successfully Been Registered Thankyou For Choosing Us'
            #Logging.send_simple_message(
                #message=message,
                #email=request.data['email'],
                #subject='Account Registration',
                #name= ""+request.data['fname']+""+request.data['lname']+""
            #)
            return Response(success)
            
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{
                'email':request.data['email'],
                'password':request.data['password']
           }
        }
        return Response(error)        



#update existing customer    
@api_view(['POST'])
def update_customer(request):    
    """
    Update Customers details
    -----
        {
            id:1,
            fname:bavon,
            lname:Okode,
            email:aokode@yahoo.com,
            msisdn:254682312,
            country_code:KE
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            customer = Customers.objects.get(id=1)
            customer.fname = request.data['fname']
            customer.lname=request.data['lname']
            customer.email=request.data['email']
            customer.msisdn=Logging.convert_numbers_to_international(request.data['msisdn'], request.data['country_code']),
            customer.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            


#update existing customer  password   
@api_view(['POST'])
def update_customer_password(request):   
    """ 
    Update User Password
    -----
        {
            id:1,
            password:123456
        } 
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            customer = Customers.objects.get(id=request.data['id'])
            customer.password = make_password(request.data['password'])
            customer.save()
            success={
                'message':'success',
                'status_code':200,
                'data':{}
            }
            return Response(success)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            



#get all existing users
@api_view(['GET'])  
def get_all_customers(request):  
    customers= Customers.objects.all()
    details=[]
    for customer in customers:
        values={
            'id':customer.id,
            'fname': customer.fname,
            'lname': customer.lname,
            'email': customer.email,
            'password': customer.password,
            'status': customer.status,
            'msisdn': customer.msisdn,
            'stripe_id': customer.stripe_id,
            'card_brand ': customer.card_brand,
            'card_last_four': customer.card_last_four,
            'trial_end_at': customer.trial_end_at,
            'created_at': customer.created_at,
            'updated_at': customer.updated_at
        }

        details.append(values)

    data={
        'data':details,
        'message':'success',
        'status_code':200
        }
    return Response(data)



#get one particelar users details
@api_view(['POST'])  
def get_particular_customer_details(request):
    if request.method == 'GET':
        success={'message':'method not allowed','status_code':401}
        return Response(success)

    elif request.method == 'POST':

        user_id=request.data['id']
        customer=Customers.objects.get(id=user_id)
        details={
            'id':customer.id,
            'fname': customer.fname,
            'lname': customer.lname,
            'email': customer.email,
            'password': customer.password,
            'status': customer.status,
            'msisdn': customer.msisdn,
            'stripe_id': customer.stripe_id,
            'card_brand ': customer.card_brand,
            'card_last_four': customer.card_last_four,
            'trial_end_at': customer.trial_end_at,
            'created_at': customer.created_at,
            'updated_at': customer.updated_at
        }

        data={'data':details,'message':'success','status_code':200}

        return Response(data)


@api_view(['DELETE'])
def delete_customer(request):
    """
    remove customer
    -----
        {
            id:customerid,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']
            stripe.api_key = STRIPE_SECRET_KEY
            get_customer=Customers.objects.get(id=_id)
            

            if get_customer.stripe_id == "0":

                delete=Customers.objects.filter(id=_id).delete()
                data={
                    "data":"user deleted",
                    "message":delete,
                    "status_code":200
                }
                return Response(data)

            else:
                cu = stripe.Customer.retrieve(get_customer.stripe_id)
                delete_stripe = cu.delete()
                delete=Customers.objects.filter(id=_id).delete()
                data={
                    "data":delete_stripe,
                    "message":delete,
                    "status_code":200
                }
                return Response(data)
        else:
            snippets={
                
                'message':"invalid request",
                "status_code":401
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)
    except:
        try:
            delete=Customers.objects.filter(id=_id).delete()
            data={
                "data":"user deleted",
                "message":delete,
                "status_code":200
            }
            return Response(data)
        except: 
            data={
                "data":{},
                "message":'user not deleted',
                "status_code":500
            }
            return Response(data)   



@api_view(['POST'])
def get_customer_email_login(request):   
    try:
        user_id=request.data['email']
        user_input_pass=request.data['password']
        customer=Customers.objects.get(email=user_id)

        if password_handler.verify(user_input_pass, customer.password):
            success={
                'data':{
                    'id':customer.id,
                    'fname': customer.fname,
                    'lname': customer.lname,
                    'email': customer.email,
                    'password': customer.password,
                    'status': customer.status,
                    'msisdn': customer.msisdn,
                    'stripe_id': customer.stripe_id,
                    'card_brand ': customer.card_brand,
                    'card_last_four': customer.card_last_four,
                    'trial_end_at': customer.trial_end_at,
                    'created_at': customer.created_at,
                    'updated_at': customer.updated_at
                    },
                'status_code':200,
            }
                
            return Response(success)

        else:
            success={
                'message':'Error',
                'status_code':500
            }
                
            return Response(success)    
     except:
        error={
            'status_code':500,
            'message':'unexpected error',
            'data':{
               
            }
        }
        return Response(error)




@api_view(['POST'])
def get_customer_cards(request):
    """
    -----
        {
            stripe_id:cus_asfhajho13
        }
    """
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        card_info = stripe.Customer.retrieve(request.data['stripe_id']).sources.all(limit=1, object='card')
        success={
            'data':card_info,
            'status_code':200,

        }
        return Response(success)
    except BaseException as e:
        error={
            'status_code':500,
            'message':'error' + str(e),
            'data':{
               
            }
        }
        return Response(error)



