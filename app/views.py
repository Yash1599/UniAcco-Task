from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import JsonResponse
from app.serializers import Profile
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import JWTSerializer, RegisterSerializer
# Create your views here.



class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'username':serializer.data.get('username')}, status=status.HTTP_201_CREATED )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                userDetail = json.pop("password")
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfilelist(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication   
    serializer_class = Profile
    def post(self ,request,format=None):
        serializer=Profile(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.status.HTTP_400_BAD_REQUEST)

class CurrentProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    
    def get(self, request, format=None):
        serializer = UserProfilelist(request.user)
        return Response(serializer.data)
