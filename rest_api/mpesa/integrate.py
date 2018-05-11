import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

MPESA_URL = "https://sandbox.safaricom.co.ke"

def getAcessToken():
    consumer_key = settings.MPESA_CONSUMER_KEY 
    consumer_secret = settings.MPESA_SECRET
    api_URL = MPESA_URL + "/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return r


def sendMoneyB2C(amount, partyB, remarks):
    access_token = getAcessToken()
    api_url = MPESA_URL +"/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "InitiatorName": "testapi0323",
        "SecurityCredential":"safaricom323!",
        "CommandID": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": "600000",
        "PartyB": partyB,,
        "Remarks": remarks,
        "QueueTimeOutURL": "http://your_timeout_url",
        "ResultURL": "http://your_result_url",
        "Occasion": " "
    }

    response = requests.post(api_url, json = request, headers=headers)

    return response


def reverse_transaction():
    access_token = getAcessToken()
    api_url = MPESA_URL +"/mpesa/reversal/v1/request"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { 
        "Initiator":" ",
        "SecurityCredential":" ",
        "CommandID":"TransactionReversal",
        "TransactionID":" ",
        "Amount":" ",
        "ReceiverParty":" ",
        "RecieverIdentifierType":"4",
        "ResultURL":"https://ip_address:port/result_url",
        "QueueTimeOutURL":"https://ip_address:port/timeout_url",
        "Remarks":" ",
        "Occasion":" "
    }

    response = requests.post(api_url, json = request, headers=headers)

    return response