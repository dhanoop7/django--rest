from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .models import CustomUser,Books,Otp

from rest_framework.views import APIView
from .serializers import CustomUserSerializer, LoginSerializer, BookSerializer, OtpSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .utils import generate_and_save_otp, send_otp_email



# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register_User(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

     
            otp_instance = generate_and_save_otp(user)

        
            send_otp_email(user.email, otp_instance)

            return Response({'message': 'OTP sent to your email. Please verify.', 'user_id':user.id})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
@permission_classes([AllowAny])
def VerifyOtp(request):
    if request.method == 'POST':
        serializer = OtpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_value = serializer.validated_data['otp']

            

            otp_instance = Otp.objects.get(user=user)

            print(user)
            print(otp_instance.otp)

            if otp_value == otp_instance.otp:
                user.is_active = True
                user.save(update_fields=['is_active'])
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token':token.key }, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid Otp'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



       
    #         otp_instance = Otp.objects.filter(user=user, otp=otp_value, verified=False).first()

    #         if otp_instance:
           
    #             otp_instance.verified = True
    #             otp_instance.save()

            
    #             authenticated_user = authenticate(request, username=user.username, password=user.password)
    #             if authenticated_user:
    #                 login(request, authenticated_user)
    #                 token, created = Token.objects.get_or_create(user=authenticated_user)

    #                 return Response({'token': token.key, 'message': 'OTP verified. User registered successfully.'})
    #             else:
    #                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    #         else:
    #             return Response({'error': 'Invalid OTP or OTP already verified'}, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
        


    
class user_Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'sucess':"Otp verified sucessfully",'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class BookView(APIView):
    def get(self, request):
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            