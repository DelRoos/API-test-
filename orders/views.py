from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import  generics, status
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from . import serializers
from .models import Order, User

# Create your views here.
class HelloOrderView(generics.GenericAPIView):
    def get(self,request):
        return Response(data={"message": "Hello order thier"}, status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):
    serializer_class= serializers.OrderCreationSerializer
    queryset=Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders=Order.objects.all()
        serializers=self.serializer_class(instance=orders, many=True)

        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        data=request.data

        serializer=self.serializer_class(data=data)
        user = request.user

        print(user.id)

        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        print("data is :", data)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    serializer_class= serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order= get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,order_id):
        data = request.data
        order= get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(data=data, instance=order)
        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order= get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateOrderStatusView(generics.GenericAPIView):
    serializer_class= serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        order=get_object_or_404(Order, pk=order_id)

        data = request.data
        serializer=self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    serializer_class= serializers.OrderDetailSerializer

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        orders=Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOrdersDetailView(generics.GenericAPIView):
    serializer_class= serializers.OrderDetailSerializer

    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)
        order=Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
