import time
import random
from celery import shared_task
from django.db import transaction
from .models import Order

@shared_task
def process_order_saga(order_id):
    try:
        with transaction.atomic():
            # Lock the order row for safety
            order = Order.objects.select_for_update().get(id=order_id)
            
            # STEP 1: Simulate Payment
            print(f"💰 Processing payment for Order {order_id}...")
            time.sleep(3) # Simulate API call
            payment_success = True # We'll assume payment always works for now
            
            if payment_success:
                # STEP 2: Simulate Inventory (The 'Chaos' Step)
                print(f"📦 Checking inventory for Order {order_id}...")
                time.sleep(3)
                
                # Let's pretend we are out of stock to test the refund!
                inventory_available = random.choice([True,False])
                
                if inventory_available:
                    order.status = 'SUCCESS'
                    print(f"✅ Order {order_id} completed!")
                else:
                    # STEP 3: The Compensating Transaction (Refund)
                    print(f"⚠️ Out of stock! Initiating refund for Order {order_id}...")
                    time.sleep(3)
                    order.status = 'REFUNDED'
            else:
                order.status = 'FAILED_PAYMENT'
            
            order.save()

    except Order.DoesNotExist:
        print(f"❌ Order {order_id} not found.")
    except Exception as e:
        print(f"🔥 Critical Error: {e}")