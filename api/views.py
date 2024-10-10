from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .helpers import check_email, is_valid_password

# Create your views here.
@api_view(['POST'])
def create_user(request):

    if request.method == 'POST':
        first_name =  request.data.get("first_name")
        last_name =  request.data.get("last_name")
        id_card_front =  request.FILES.get("id_card_front") 
        id_card_back =  request.FILES.get("id_card_back") 
        ssn =  request.data.get("ssn") 
    
        email = request.data.get("email")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        if password != password_confirm:
            return Response({
                "detail": "Passwords must match."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({
                "detail": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({
                "detail": "Password is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if email and password are valid entry
            email_valid_status = check_email(email)
            password_valid_status = is_valid_password(password)

            if password_valid_status.status == False:
                return Response({
                    "detail": "".join([
                        error_message for error_message in password_valid_status.error_messages
                    ])
                }, status=status.HTTP_400_BAD_REQUEST)

            if email_valid_status.status == False:
                return Response({
                    "detail": "".join([
                        error_message for error_message in email_valid_status.error_messages
                    ])
                }, status=status.HTTP_400_BAD_REQUEST)
            
        
            
    return Response({"message": "This is working"})


