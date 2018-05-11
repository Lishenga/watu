from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Transactions, Forex
from django.core.serializers import serialize
import datetime
import http.client
import json
from django.http import HttpResponse
from . import Logging
from pprint import pprint
from django.conf import settings
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

#STRIPE_SECRET_KEY = "sk_test_hQcwVNlTH1MDVLggM1avFWr4"
FOREX_TRADING_KEY="0522e173fb713aa5542cfd0842a76850"


def convert_and_send(self):
    data = Logging.save_rates()
    forex= Forex(
        source="USD", 
        quote="USDKES", 
        amount=data['quotes']['USDKES'],
        created_at = datetime.date.today(),
        updated_at= datetime.date.today())
    forex.save()
    success={
            "data":data['quotes']['USDKES'],
            "message":"success",
            "status_code":200
        } 
    return HttpResponse(json.dumps(success), content_type="application/json")


@api_view(['POST'])
def convert_and_send_actual(request):
    """
    Initiate a send amaoney Transaction

    -----
    {
        transation:1,
    }
    """
    transaction=request.data['transaction']

    find_transaction=Transactions.objects.get(id=transaction)

    data=Logging.convert_currency(_from="USD", to="KES", amount=find_transaction.Amount)
    send_money=Logging.send_money_MPESA(number=find_transaction.Receiver, amount=data)

    if send_money['status_code'] == 200:
        find_transaction.status = 1
        find_transaction.updated_at = datetime.date.today()
        find_transaction.save()
        success={
                "message":"success",
                "status_code":200
            } 
        return Response(success)

    else:
        success={
                "message":"error",
                "status_code":500
             } 

        return Response(success)  


@api_view(['GET'])
def get_all_transactions(request):
    try:
        transactions= Transactions.objects.all()
        details=[]
        for transaction in transactions:
            values={
                'id':transaction.id,
                'from':transaction.Sender,
                'to':transaction.Receiver,
                'amount':transaction.Amount,
                'created_at': transaction.created_at,
                'updated_at': transaction.updated_at
            }
            details.append(values)

        data={
                'data':details,
                'message':'success',
                'status_code':200
            }
        return Response(data)  

    except:
        error={
            'status_code':500,
            'message':'tyr',
            'data':{}
        }
        return Response(error)    





@api_view(['POST'])
def get_customer_transactions(request):  
    """
    Get Customer Transactions
    -----
        {
            number:25453287,
        }

    """
    try:
        transactions= Transactions.objects.filter(Receiver=request.data['number']) | Transactions.objects.filter(Sender=request.data['number'])
        details=[]
        for transaction in transactions:
            values={
                'id':transaction.id,
                'from':transaction.Sender,
                'to':transaction.Receiver,
                'amount':transaction.Amount,
                'created_at': transaction.created_at,
                'updated_at': transaction.updated_at
            }
            details.append(values)

        data={
            'data':details,
            'message':'success',
            'status_code':200}
        return Response(data)  

    except:
        error={
            'status_code':500,
            'message':'tyr',
            'data':{}
        }
        return Response(error)      

                        
         
   

    



        
    

