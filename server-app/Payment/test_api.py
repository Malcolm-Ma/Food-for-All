import requests
import json

client_id = 'AT96y4XONeD0OK88DlwW43rU3sSw9lH55Yfz3etD0RvFtTVfoUbwIpMebVjRxkmEeyFf5ycl7Xp7gU1l'
secret = 'EFC8hviHQf2sFY-hl_IRkg-4mPclc5dfPxlnN6Vz70F8SHf9-hCImLfaBjqTk4m5_pXb7IujTpqo0JF-'

##Authorization
def paypal_authorization(client_id=client_id, secret=secret):
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data, auth=(client_id, secret))
    response_dict = json.loads(response.content)
    return response_dict

##List products
def paypal_list_products(authorization_dict):
    params = {'page_size': '2', 'page': '1', 'total_required': 'true'}
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, params=params)
    response_dict = json.loads(response.content)
    return response_dict

product_dict = {
    'name': 'Video Streaming Service',
    'description': 'Video streaming service',
    'type': 'CHARITY',
    'category': 'SOFTWARE',
    'image_url': 'https://example.com/streaming.jpg',
    'home_url': 'https://example.com/home',
}

def paypal_create_product(authorization_dict, product_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer Access-Token', 'PayPal-Request-Id': 'PRODUCT-18062020-001'}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, json=product_dict)
    response_dict = json.loads(response.content)
    return response_dict