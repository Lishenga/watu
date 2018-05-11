from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Countries, Forex
from django.core.serializers import serialize
import datetime
import json

@api_view(['POST'])
def create_rate(request):
    """
    Create New Rate
    -----
        {
            high:USD,
            low:KES,
            buying:101,
            selling:120,
        }
    """
    try:

        forex = Forex(
            high = request.data['high'],
            low = request.data['low'],
            buying = request.data['buying'],
            selling = request.data['selling'],
            quote = request.data['high']+':'+request.data['low'],
            created_at = datetime.date.today(),
            updated_at= datetime.date.today()
        )

        forex.save()

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
def update_rate(request):
    """
    Update Rate
    -----
        {
            id:1,
            high:USD,
            low:KES,
            buying:101,
            selling:120,
        }
    """
    try:
        forex = Forex.object.get(id=request.data['id'])
        forex.high = request.data['high']
        forex.low = request.data['low']
        forex.buying = request.data['buying']
        forex.selling = request.data['selling']
        forex.quote = request.data['high']+':'+request.data['low']
        forex.updated_at= datetime.date.today()
        forex.save()

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
def view_rates(request):
    """
    View All Countries
    -----
       
    """
    try:
        forex = Forex.objects.all()
        data = []

        for forn in forex:
            data.append({
                'id':forn.id,
                'high':forn.high,
                'low':forn.high,
                'buying':forn.buying,
                'selling':forn.selling,
                'created_at':forn.created_at,
                'updated_at':forn.updated_at  
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


@api_view(['GET'])
def get_particular_rate(request):
    """
    Get Particular Rate Details
    ----
        {
            high:USD,
            low:KES
        }
    """

    try:

        high = request.data['high']
        low  = request.data['low']
        result = check_rate_exsistence(high, low)
        return Response(result) 

    except BaseException as e:

        error = {
                'message':'error:'+ str(e),
                'data':{},
                'status_code':500
            }
                
        return Response(error) 
    



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

    
