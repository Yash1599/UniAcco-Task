from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import JsonResponse

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

    # def post(self, request, format='json'):
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         if user:
    #             json = serializer.data
    #             userDetail = json.pop("password")
    #             return Response(json, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    