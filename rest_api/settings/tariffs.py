from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Tariffs
from django.core.serializers import serialize
import datetime
import json

@api_view(['POST'])
def create_rate_mpesa(request):
    """
    Create Mpesa Tarrif
    -----
        {
            Max:KES,
            Min:KES,
            tariff_type:ERTTGH7889,
            amount:120,
        }
    """
    try:

        mpesa_tarrif = Tariffs(
            minimum = request.data['Min'],
            maximum = request.data['Max'],
            amount = request.data['amount'],
            tariff_type = request.data['tariff_type'],
            created_at = datetime.date.today(),
            updated_at= datetime.date.today()
        )

        mpesa_tarrif.save()

        return Response({
            'message':'success',
            'data':{},
            'status_code':200
        })
    
    except BaseException as e:

        return Response({
            'message':'error' + str(e),
            'data':{},
            'status_code':500
        })

@api_view(['PUT'])
def mpesa_tariff_update(request):
    """
    Update Mpesa Tarrif
    -----
        {
            id:1
            Max:KES,
            Min:KES,
            tariff_type:ERTTGH7889,
            amount:120,
        }
    """
    try:
        Mpesa_tarrif = Tariffs.objects.get(id=request.data['id'])
        Mpesa_tarrif.minimum = request.data['Min']
        Mpesa_tarrif.maximum = request.data['Max']
        Mpesa_tarrif.amount = request.data['amount']
        Mpesa_tarrif.tariff_type = request.data['tariff_type']
        Mpesa_tarrif.updated_at= datetime.date.today()
        Mpesa_tarrif.save()

        return Response({
            'message':'success',
            'data':{},
            'status_code':200
        })

    except BaseException as e:

        return Response({
            'message':'error' + str(e),
            'data':{},
            'status_code':500
        })

@api_view(['GET'])
def mpesa_view_tariffs(request):
    """
    View All Mpesa Tariffs
    -----
       
    """
    try:
        Mpesa_tariffs = Tariffs.objects.all()
        data = []

        for tar in Mpesa_tariffs:
            data.append({
                'id':tar.id,
                'max':tar.maximum,
                'min':tar.minimum,
                'amount':tar.amount,
                'tariff_type':tar.tariff_type,
                'created_at':tar.created_at,
                'updated_at':tar.updated_at  
            })

        return Response({
                'message':'success',
                'data':data,
                'status_code':200
            }) 

    except BaseException as e:
        error = {
                'message':'error:'+ str(e),
                'data':{},
                'status_code':500
            } 
                
        return Response(error) 

@api_view(['POST'])
def mpesa_get_particular_tariff(request):
    """
    Get Particular Mpesa Tariff Details
    ----
        {
            Amount:KES,
        }
    """

    am=request.data['amount']
    Mpesa_tariffs = Tariffs.objects.all()
    data = []

    for tariffs in Mpesa_tariffs:
        if(int(tariffs.maximum) >= int(am) and int (tariffs.minimum) <= int(am)):
            data.append({
                'id':tariffs.id,
                'max':tariffs.maximum,
                'min':tariffs.minimum,
                'amount':tariffs.amount,
                'tariff_type':tariffs.tariff_type,
                'created_at':tariffs.created_at,
                'updated_at':tariffs.updated_at  
            })
            
    return Response({
            'message':'success',
            'data':data,
            'status_code':200
        }) 

@api_view(['DELETE'])
def delete_mpesa_tariff(request):
    """
    Delete Mpesa Tariff
    -----
        {
            id:1,
        }
    """
    try:
        Tariffs.objects.filter(id=request.data['id']).delete()
        return Response({
            'message':'success',
            'data':{},
            'status_code':200
        })

    except BaseException as e:
        error = {
                'message':'error:'+ str(e),
                'data':{},
                'status_code':500
            }
                
        return Response(error) 

@api_view(['DELETE'])
def delete_all_mpesa_tariffs(request):
    """
    Delete Mpesa All Tariffs
    
    """
    try:
        Tariffs.objects.all().delete()
        return Response({
            'message':'success',
            'data':{},
            'status_code':200
        })

    except BaseException as e:
        error = {
                'message':'error:'+ str(e),
                'data':{},
                'status_code':500
            }
                
        return Response(error) 
