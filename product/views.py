from django.shortcuts                       import render
from rest_framework.views                   import APIView
from .serializers                           import RegisterSerializer, UserSerializer
from rest_framework.response                import Response
from rest_framework                         import status
from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer
from .models                                import User
# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            #쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다. 
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AuthView(APIView):

    def post(self, request):
        username = request.data['login_id']
        password = request.data['password']
        user = User.objects.filter(login_id=username).first()
        
        
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        return Response(
            {
                "user": serializer.data,
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                 },
            }
        )