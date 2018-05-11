from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Customers, Cards, Transactions, Countries
from django.core.serializers import serialize
from lipisha import Lipisha
import datetime
import stripe
import http.client
import json
from . import Logging
from django.conf import settings
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

#STRIPE_SECRET_KEY = "sk_test_hQcwVNlTH1MDVLggM1avFWr4"



#LIPISHA_API_KEY = "830647cb47a27787b90dc01b950bfb28"
#LIPISHA_API_SIGNATURE = "sVoXhqxFi+p6pvln4hEy5JBqOkPmgaiS3nqJlL6e5mNBkHm6cR7aLXg73lF1uWsJW3Ou6TaFEYP4OQZ1XD4MrJ0VJk6w7dq6SRMxehwhM6A+GrdMxNnCkWVWuCLVfYO6QDg6/vLy21CU27rhj7EhNtqq8/rMHJHxSpafVc4vNSk="
LIPISHA_API_KEY = "c3f84698ee3d844bb11f0955f9cfe335"
LIPISHA_API_SIGNATURE = "ePgW9Ii1gtxYnZ3bHGAGX0YsFKy+b+VgeCxD74H1mLbOuhCes7qhJMhNY2Wf6abtmv2kTaUeYeayhEYO0/aALlHC3Mty3oiRSWQirX5SegApjWgyIqIg/D4eWCMp1SflnC0tFjpJxTMpKz6aeSkeTXKEH93rSsfxm91pG2ZyK2c="

@api_view(['POST'])
def disburse_cash_MPESA(request):
    """
    Send Money from Our Lipisha Accoount To  Phone
    -----
        {
            amount:100,
            phone:25412345678,
        }
    
    
    """
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':      
        api_key = LIPISHA_API_KEY
        api_signature = LIPISHA_API_SIGNATURE
        lipisha = Lipisha(api_key, api_signature, api_environment='live')
        send_money=lipisha.send_money(
            account_number="10966",
            mobile_number=request.data['phone'], 
            amount=request.data['amount']
        )
        
        success={
            "data":send_money,
            "message":"success",
            "status_code":200
            } 

        return Response(success) 



@api_view(['POST'])
def lipisha_account_balance(request):
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST': 
        api_key = LIPISHA_API_KEY
        api_signature = LIPISHA_API_SIGNATURE
        lipisha = Lipisha(api_key, api_signature, api_environment='live') 
        balance=lipisha.get_float(account_number="10969")
        success={"data":balance,
                "message":"success",
                "status_code":200
                } 
        return Response(success) 



@api_view(['POST'])
def lipisha_confirm_transactions(request):
    """
    Confirm Transaction Is Ok
    -----
        {
            transaction:895662266
        }
    
    
    
    """
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST': 
        api_key = LIPISHA_API_KEY
        api_signature = LIPISHA_API_SIGNATURE
        lipisha = Lipisha(api_key, api_signature, api_environment='live') 
        confirm=lipisha.acknowledge_transaction(transaction=request.data['transaction'])
        success={
            "data":confirm,
            "message":"success",
            "status_code":200
            } 

        return Response(success) 


@api_view(['POST'])
def lipisha_get_transactions(request):
    """
    Get list of Transactions
    
    """
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST': 
        api_key = LIPISHA_API_KEY
        api_signature = LIPISHA_API_SIGNATURE
        lipisha = Lipisha(api_key, api_signature, api_environment='live') 
        confirm=lipisha.get_transactions()
        success={
            "data":confirm,
            "message":"success",
            "status_code":200
            } 

        return Response(success) 


@api_view(['POST'])
def create_lipisha_account(request):
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        conn = http.client.HTTPConnection("https://api.lipisha.com")
        payload = {
                "api_key": LIPISHA_API_KEY,
                "api_signature": LIPISHA_API_SIGNATURE,	
                "account_number": "09250",
                "mobile_number": 254702759950,	
                "amount": 50,
                "currency":	"KES",
                "reference": "CODE23524"	
        }

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            }

        conn.request("POST", "/v2/send_money/", json.dumps(payload).encode("utf-8"), headers)
        res = conn.getresponse()
        data = res.read()

        
        success={"data":data.decode("utf-8"),
                "message":"success",
                "status_code":200
                } 

        return Response(success) 


####stripe integration methods
####
@api_view(['POST'])
def create_stripe_customer(request): 
    """
    create a stripe account for existing Watu User

    -----
        {
            email:example@gmail.com,
        }
    """
    if request.method == 'GET':
        snippets='success'
        return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        email = request.data['email']
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

            return Response(success)  

        else:  
            success={
                        "message":"customer already exists",
                        "status_code":200
                    } 

            return Response(success)  

                
             


@api_view(['POST'])
def create_stripe_customer_card(request): 
    """
    Create Stripe Customers Card
    -----
        {
            email:useremail,
            number:424242424242424,
            exp_month:07,
            exp_year:22,
            cvc:494
        }

    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':     
            email = request.data['email'] 
            card = {
                "number": request.data['number'] ,
                "exp_month": request.data['exp_month'],
                "exp_year": request.data['exp_year'],
                "cvc": request.data['cvc']
            }
            stripe.api_key = STRIPE_SECRET_KEY
            customer = Customers.objects.get(email=email)
            token = stripe.Token.create(card=card, api_key=STRIPE_SECRET_KEY)  
            customer = stripe.Customer.retrieve(customer.stripe_id)
            create_card=customer.sources.create(source= token['id'])
            
            success={
                    "data":create_card,
                    "message":"success",
                    "status_code":200
                } 
            return Response(success)  
    except BaseException as e:

        error={
            'data':[],
            'message':'error'+ str(e),
            'status_code':500
        }

        return Response(error)  



@api_view(['POST'])
def create_stripe_customer_charge(request): 
    """
    Charge Card for Stripe check out

    -----
        {
            email:example@gmail.com,
            amount:50,
            number:2321441,
            currency:USD
        }
      
    """
    try:
        email = request.data['email'] 
        customer = Customers.objects.get(email = email)
        currency = request.data['currency']
        _receiver = Customers.objects.get(msisdn = request.data['number'])
        _receiver_currency = Countries.objects.get( country_code = _receiver.country_code)

        converted_amount = Logging.convert_currency(_from = currency, to = _receiver_currency , amount = request.data['amount'])


        stripe.api_key = STRIPE_SECRET_KEY

        stripe_charge = stripe.Charge.create(
                amount = int(request.data['amount'])*100,
                currency = request.data['currency'],
                customer = customer.stripe_id,
                description="Charge to Send Money",
            )

        if stripe_charge['status']=="succeeded":

            transaction = Logging.create_transaction(
                _from=customer.msisdn,
                to = request.data['number'], 
                amount = int(request.data['amount'])
            )

            transaction_data = {

                "id":transaction.id,
                "from":transaction.Sender,
                "to":transaction.Receiver,
                "amount":transaction.Amount
            } 

            send_money = Logging.send_money_receiver(number = transaction.Receiver, amount = converted_amount, country = _receiver.country_code)
            sms_data = Logging.send_sms(number = transaction.Receiver, text="amount sent")


            if send_money["status_code"]==200:
                
                success=  { 
                    "data":{
                        "sms_data":sms_data,
                        "transaction_data":transaction_data,
                        "send_data":send_money,
                    },
                    "message":"success",
                    "status_code":200
                } 
                return Response(success)

            else:

                error={
                        'message':'could not send money to MPESA',
                        'data':[],
                        'status_code':500
                }
                return Response(error)   

        else:
            error={
                'message':'could not charge account',
                'data':[],
                'status_code':500
            }

            return Response(error)  


    except BaseException as e:
        
        error={
            'data':[],
            'message':'error'+ str(e),
            'status_code':500
        }

        return Response(error)  


                
                        
               
@api_view(['GET'])
def get_stripe_balance(request): 
    stripe.api_key = STRIPE_SECRET_KEY

    balance=stripe.Balance.retrieve()
    success={
        "data":balance,
        "message":"success",
        "status_code":200
        } 
    return Response(success)   


@api_view(['POST'])
def test_africa_send_money(request): 
    info = Logging.send_money_MPESA_africastalking(number=request.data['number'], amount=request.data['amount'])

    return Response(info)   
    
