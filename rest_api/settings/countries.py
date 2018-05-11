from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Settings, Countries
from django.core.serializers import serialize
import datetime
import stripe
import http.client
import json
from django.conf import settings

@api_view(['POST'])
def create_country(request):
    """
    Create Country
    -----
        {
            name:string,
            country_code:string,
            currency_code:string

        }
    """
    try:
        country = Countries(
            name=request.data['name'],
            country_code=request.data['country_code'],
            currency_code=request.data['currency_code'],
            created_at=datetime.date.today(),
            updated_at=datetime.date.today()
        )

        country.save()

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

    


@api_view(['GET'])
def view_country(request):
    """
    View All Countries
    -----
       
    """
    try:
        countries = Countries.objects.all()
        data = []

        for country in countries:
            data.append({
                'id':country.id,
                'name':country.name,
                'country_code':country.country_code,
                'currency_code':country.country_code
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
    

   

@api_view(['DELETE'])
def delete_country(request):
    """
    Delete Countries
    -----
        {
            id:1,
        }
    """
    try:
        Countries.objects.filter(id=request.data['id']).delete()
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

   


@api_view(['PUT'])
def update_country(request):
    """
    Update Country
    -----
        {
            id:int,
            name:string,
            country_code:string,
            currency_code:string

        }
    """
    try:
        country = Countries.objects.get(id=1)
        country.name = request.data['name']
        country.country_code = request.data['country_code']
        country.currency_code = request.data['currency_code']
        country.updated_at = datetime.date.today()
        country.save()

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