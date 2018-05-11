from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_api.models import  Chats, Messages, SocketDetails
from django.contrib.auth.hashers import make_password
from passlib.hash import django_pbkdf2_sha256 as password_handler

import random
import string
import datetime


@api_view(['POST'])
def send_message(request):
      """
      Sample
      -----
            {
                  sender:player_id,
                  receiver:player_id,
                  chat_id:chat_id,
                  message:message,
            }
      """
      try:
            sender=request.data['sender']
            receiver=request.data['receiver']
            chat_id=request.data['chat_id']
            message=request.data['message']
            
            create = Messages(
                  sender=sender, 
                  receiver=receiver, 
                  chat_id=chat_id, 
                  message=message, 
                  created_at = datetime.date.today(),
                  updated_at= datetime.date.today())
            create.save()
            return Response({
                  'message':'success',
                  'status_code':200
            }) 

      except BaseException as e:   
            error = {
                        'message':'error:'+ str(e),
                        'status_code':500
                  }
                  
            return Response(error) 



@api_view(['POST'])
def get_messages(request):
      """
      chat_id---chat id
      """
      try:
            details=[]
            messages=Messages.objects.filter(chat_id=request.data['chat_id']).order_by('id')
            for ch in messages:
                  values={
                        'id':ch.id,
                        'chat_id':ch.chat_id,
                        'sender':ch.sender,
                        'receiver':ch.receiver,
                        'message':ch.message,
                        'created_at': ch.created_at,
                        'updated_at': ch.updated_at
                  }
                  details.append(values)
            return Response({
                  'data':details,
                  'status_code':200,
                  'message':'success'
            }) 
      except BaseException as e:   
            error = {
                  'message':'error:'+ str(e),
                  'status_code':500
                  }
                  
      return Response(error)





@api_view(['POST'])
def load_chat(request):
      """
      
      Load All Chat Information
      -----
            {
                  member_1:player_id,
                  member_2:player_id_2
            }
     
      """
      try:
            member_1=request.data['member_1']
            member_2=request.data['member_2']

            chat= Chats.objects.filter(member_1=member_1, member_2=member_2)
            chat_2= Chats.objects.filter(member_1=member_2, member_2=member_1)
            details=[]
            if not chat:
                  if not chat_2:
                        random=random_string()
                        create=Chats(
                              member_1=member_1,
                              member_2=member_2, 
                              chat_id=random, 
                              created_at = datetime.date.today(),
                              updated_at= datetime.date.today()
                              )
                        create.save()
                        for ch in Chats.objects.filter(member_1=member_1, member_2=member_2):
                              values={
                                    'id':ch.id,
                                    'chat_id':ch.chat_id,
                                    'member_1':ch.member_1,
                                    'member_2':ch.member_2,
                                    'created_at': ch.created_at,
                                    'updated_at': ch.updated_at
                              }
                              details.append(values)

                        return Response({
                              'data':details[0],
                              'status_code':200,
                              'message':'attempt 2'
                        }) 
                  else:
                        for ch in chat_2:
                              values={
                                    'id':ch.id,
                                    'chat_id':ch.chat_id,
                                    'member_1':ch.member_1,
                                    'member_2':ch.member_2,
                                    'created_at': ch.created_at,
                                    'updated_at': ch.updated_at
                              }
                              details.append(values)

                        return Response({
                              'data':details[0],
                              'status_code':200,
                              'message':'attempt 3'
                        })     
            else:      
                  for ch in chat:
                        values={
                              'id':ch.id,
                              'chat_id':ch.chat_id,
                              'member_1':ch.member_1,
                              'member_2':ch.member_2,
                              'created_at': ch.created_at,
                              'updated_at': ch.updated_at
                        }
                        details.append(values)

                  return Response({
                        'data':details[0],
                        'status_code':200,
                        'message':'attempt 1'
                  })   

      except BaseException as e:   

            error = {
                  'message':'error:'+ str(e),
                  'status_code':500
                  }
                  
            return Response(error)           


@api_view(['POST'])
def set_player_details(request):
      """
      
      Set One Signal Player Details
      -----
           {
                  msisdn:phone number,
                  player_id:player_id_2
           }
     
      """
      try:
            msisdn=request.data['msisdn']
            player_id=request.data['player_id']

            create =  SocketDetails(
                  msisdn=msisdn,
                  player_id=player_id
            )
            create.save()
            return Response({
                  'message':'success',
                  'status_code':200
            }) 
      except:
            error = {
                  'message':'error:',
                  'status_code':500
                  }
                  
            return Response(error) 



@api_view(['POST'])
def get_player_details(request):
      """
      Get Particular Player Details
      -----
            {
                  msisdn:phone number
            }

      """
      msisdn=request.data['msisdn']
      try:
            player = SocketDetails.objects.get(msisdn=msisdn)
            details = {
                  'msisdn':player.msisdn,
                  'player_id':player.player_id
            }
            return Response({
                  'message':'success',
                  'status_code':200,
                  'data':details
            }) 


      except:
            error = {
                  'message':'error:',
                  'status_code':500
                  }   
            return Response(error) 




def random_string():
      char_set = string.ascii_uppercase + string.digits
      return ''.join(random.sample(char_set*6, 6))