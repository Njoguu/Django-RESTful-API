from msilib import type_string
from webbrowser import get
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # send email-activation email
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        currentsite = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        absolute_url = 'https://' + currentsite + relativeLink + '?token=' + str(token)

        email_body = 'Hello ' + user.username + '. Please click on the link below to verify your email and activate your account \n' + absolute_url

        data = {
            'email_body' : email_body,
            'to_email' : user.email,
            'email_subject' : 'Verify your Email'
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED) # -->returns response that user has been created

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])

    def get(self, request):
        token = request.GET.get('token') 
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email':'Successfully Activated!'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation link has expired!'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token, please request a new one!'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
