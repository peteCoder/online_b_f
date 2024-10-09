from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .helpers import check_email, is_valid_password

# Create your views here.
@api_view(['POST'])
def create_user(request):

    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        if not email:
            return Response({
                "message": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({
                "password": "Password is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if email and password are valid entry
            email_valid_status = check_email(email)
            password_valid_status = is_valid_password(password)
            if email_valid_status.status == False:
                return Response({
                    "email": [
                        error_message for error_message in email_valid_status.error_messages
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "This is working"})


