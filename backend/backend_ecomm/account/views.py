from rest_framework import status
from django.shortcuts import render 
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer,LogoutSerializer,CustomTokenObtainPairSerializer,UserDetailSerializer
from .models  import User




class RegisterUserViewSet(viewsets.ViewSet):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['data']=serializer.data
            context['message'] = "user created"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        context={}
        serializer=LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh']
            try :
                token = RefreshToken(refresh_token)
                token.blacklist()
                context['data']={}
                context['message'] = "user logout"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            except:
                context['data']={}
                context['message'] = "user  already Logged out "
                context['status']=False
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class TokenObtainPairPatchedView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

class UserDetailViewSet(viewsets.ViewSet):

    serializer_class = UserDetailSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        context={}
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        context['data']=serializer.data
        context['message'] = "all user data"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request,pk=None):
        context={}
        try :
            serializer = self.serializer_class(request.user)
            context['data']=serializer.data
            context['message'] = "user detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "user detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



    