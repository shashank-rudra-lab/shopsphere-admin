from flask import Flask, render_template
import requests
from auth_helper import get_service_account_token


app = Flask(__name__)

# API Gateway URL
API_GATEWAY_URL = 'https://shopsphere-gateway-46h5n97t.uc.gateway.dev'

@app.route('/')
def home():
    # Fetch product info from API Gateway
    products_resp = requests.get(f'{API_GATEWAY_URL}/products')
    products = products_resp.json() if products_resp.ok else []

      # Fetch shipping in progress from API Gateway (secure)
    id_token_jwt = get_service_account_token()
    secure_headers = {'Authorization': f'Bearer {id_token_jwt}'}
    orders_resp = requests.get(f'{API_GATEWAY_URL}/orders/shipping_in_progress', headers=secure_headers)
    shipping_list = orders_resp.json() if orders_resp.ok else []
    # Convert shipping list to dict for easy lookup
    shipping_data = {}
    for item in shipping_list:
        shipping_data[str(item.get("product_id"))] = item.get("shipping_in_progress", 0)

    # Fetch stock available from API Gateway
    inventory_resp = requests.get(f'{API_GATEWAY_URL}/inventory')
    inventory_json = inventory_resp.json() if inventory_resp.ok else {}
    inventory_data = {}
    # Convert inventory list to dict for easy lookup
    for item in inventory_json.get("inventory", []):
        inventory_data[item.get("product_id")] = item.get("stock", "Unknown")

    # Merge data for display
    merged_products = []
    for product in products:
        product_id = str(product.get('product_id'))
        merged_products.append({
            "product_id": product_id,
            "name": product.get('name'),
            "image_url": product.get('image_url'),
            "price": product.get('price'),
            "shipping_in_progress": shipping_data.get(product_id, 0),
            "stock_available": inventory_data.get(product_id, "Unknown")
        })

    return render_template('index.html', products=merged_products)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 