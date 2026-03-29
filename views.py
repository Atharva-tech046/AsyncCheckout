from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Add RetrieveAPIView to your imports
from rest_framework.generics import RetrieveAPIView 
from .models import Order
from .serializers import OrderSerializer
from .tasks import process_order_saga

# Your existing view
class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Save the order
            order = serializer.save()
            
            # 2. Trigger the background task
            process_order_saga.delay(order.id)
            
            # 3. Return the receipt
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🆕 Add this new view for Polling
class OrderStatusView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['GET', 'DELETE'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        count = Order.objects.all().delete()
        return Response(
            {"message": f"Successfully deleted {count[0]} orders. Database is clean!"}, 
            status=status.HTTP_204_NO_CONTENT
        )