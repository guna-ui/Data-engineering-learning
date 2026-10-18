
import json
from pathlib import Path


base_dir=Path(__file__).resolve().parent




def extract_order_summary(order: dict) -> dict:

    def get_amount(order):
       line_items=order.get('line_items') or []
       total = 0.0
       for item in line_items:
          total += item.get("price", 0.0) * item.get("qty", 0)
       return total
    customer = order.get('customer') or {}
    shipping = order.get('shipping') or {}
    address = shipping.get('address') or {}
    return {
    'order_id': order.get('order_id'),
    'customer_name': customer.get('name', 'Guest'),
    'customer_email': customer.get('email', 'N/A'),
    'city': address.get('city', 'No Shipping'),
    'total_amount': get_amount(order)
}


if __name__ == "__main__":
    file_path=base_dir/'orders_dump.json'
    print(file_path)
    with open(file=file_path,mode='r',encoding='utf-8') as f:
        orders=json.load(f)
    for order in orders:
     print(extract_order_summary(order=order))
        # extract_order_summary(order=order)