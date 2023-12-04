from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Product
from .serializers import ProductSerializer,ProductSerializerList


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Product.objects.get(id=pk)
        except :
            context['data']={}
            context['message'] = "product detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializerList(queryset,context={'request': request})
        context['data']=serializer.data
        context['message'] = "product detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    def list(self, request):
        context={}
        queryset = Product.objects.all()
        serializer = ProductSerializerList(queryset, many=True, context={"request": request})
        context['data']=serializer.data
        context['message'] = "all artist detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "product created"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
 
    def partial_update(self, request, pk=None):
        context={}
        try :
            queryset=Product.objects.get(id=pk)
            serializer = self.serializer_class(queryset,data=request.data,context={"request":request},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']=serializer.data
                context['message'] = "product detail updated"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except :
            context['data']={}
            context['message'] = "product detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        context={}
        try:
            Product.objects.get(id=pk).delete()
            context['data']={}
            context['message'] = "product successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    