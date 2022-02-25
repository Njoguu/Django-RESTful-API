from webbrowser import get
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass 

