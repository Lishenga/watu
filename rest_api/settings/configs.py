from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import Settings
from django.core.serializers import serialize
import datetime
import stripe
import http.client
import json
from django.conf import settings


STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

@api_view(['PUT'])
def set_default_tariff_percentage(request):
    """
    Set Default Exbange percentage for watu tariff
    -----
        {
            value:3,
        }
    """

    try:
        success={
            'message':'success',
            'data':[],
            'status_code':200,
        }

        setting = Settings.objects.get(name='DEFAULT_SETTINGS_PERCENTAGE')
        setting.value=request.data['value']
        setting.save()

        return Response(success)
    except BaseException as e:
        error={
            'message':'error '+ str(e),
            'data':[],
            'status_code':500,
        }
        return Response(error)



@api_view(['POST'])
def set_default_currency(request):
    """
    Set Default Core Currency
    -----
        {
            value:3,
        }
    """

    try:
        success={
            'message':'success',
            'data':[],
            'status_code':200,
        }

        setting = Settings.objects.get(name='DEFAULT_CURRENCY')
        setting.value=request.data['value']
        setting.save()

        return Response(success)
    except BaseException as e:
        error={
            'message':'error '+ str(e),
            'data':[],
            'status_code':500,
        }
        return Response(error)

