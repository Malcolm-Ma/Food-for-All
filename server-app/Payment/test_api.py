import requests
import json

client_id = 'AT96y4XONeD0OK88DlwW43rU3sSw9lH55Yfz3etD0RvFtTVfoUbwIpMebVjRxkmEeyFf5ycl7Xp7gU1l'
secret = 'EFC8hviHQf2sFY-hl_IRkg-4mPclc5dfPxlnN6Vz70F8SHf9-hCImLfaBjqTk4m5_pXb7IujTpqo0JF-'

#def check_token_valid():
#    response_dict = json.loads(response.content)
#    if response.status_code == 401 and response_dict["error"] == "invalid_token":
#        pass

#Authorization
def paypal_authorization(client_id=client_id, secret=secret):
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data, auth=(client_id, secret))
    response_dict = json.loads(response.content)
    return response_dict

pp_authorization_dict = paypal_authorization()

#List products

list_products_params = {'page_size': '2', 'page': '1', 'total_required': 'true'}

def paypal_list_products(authorization_dict, list_products_params):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, params=list_products_params)
    response_dict = json.loads(response.content)
    return response_dict

pp_products_list = paypal_list_products(pp_authorization_dict, list_products_params)

#Create product
create_product_dict = {
    'name': 'apex test',
    'description': 'food for all',
    'type': 'SERVICE',
    'category': 'CHARITY',
    'image_url': 'https://example.com/streaming.jpg',
    'home_url': 'http://127.0.0.1:8000/admin/',
}

def paypal_create_product(authorization_dict, create_dict):
    headers = {'Prefer': 'return=representation', 'PayPal-Request-Id': 'PRODUCT-18062020-001', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, json=create_dict)
    response_dict = json.loads(response.content)
    return response_dict

pp_create_product = paypal_create_product(pp_authorization_dict, create_product_dict)

#Update product
update_product_dict = [
    {
        'op': 'replace',
        'path': '/description',
        'value': 'FOOD FOR ALL',
    },
    {
        'op': 'replace',
        'path': '/image_url',
        'value': 'https://example.com/streaming1.jpg',
    },
    {
        'op': 'replace',
        'path': '/home_url',
        'value': 'http://127.0.0.1:8000/static/apidoc/index.html',
    },
]

def paypal_update_product(authorization_dict, product_id, update_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.patch('https://api-m.sandbox.paypal.com/v1/catalogs/products/{product_id}'.format(product_id=product_id), headers=headers, json=update_dict)
    if response.status_code == 204:
        return True
    else:
        return False

pp_update_product = paypal_update_product(pp_authorization_dict, pp_create_product["id"], update_product_dict)

#Show product details

def paypal_show_product(authorization_dict, product_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/catalogs/products/{product_id}'.format(product_id=product_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_product = paypal_show_product(pp_authorization_dict, pp_create_product["id"])

#Create order

order_data = {
    'intent': 'CAPTURE',
    'purchase_units': [
        {
            'amount': {
                'currency_code': 'CAD',
                'value': '22.00',
            },
        },
    ],
    "application_context": {
        "return_url": "http://127.0.0.1:8000/admin/",
        "cancel_url": "http://127.0.0.1:8000/static/apidoc/index.html"
    },
    "payment_instruction": {
        "platform_fees": [
          {
            "amount": {
              "currency_code": "CAD",
              "value": "0.00"
            },
          }
        ],
    },
}

def paypal_create_order(authorization_dict, order_data):
    headers = {
        'Prefer': 'return=representation',
        'Content-Type': 'application/json',
        'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"]),
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=order_data)
    response_dict = json.loads(response.content)
    return response_dict

pp_create_order = paypal_create_order(pp_authorization_dict, order_data)

#Show order details

def paypal_show_order(authorization_dict, order_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}'.format(order_id=order_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_order = paypal_show_order(pp_authorization_dict, pp_create_order["id"])

#Authorize payment for order

def paypal_authorize_order(authorization_dict, order_id):
    headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/authorize'.format(order_id=order_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_authorize_order = paypal_authorize_order(pp_authorization_dict, pp_create_order["id"])

#Capture payment for order

def paypal_capture_order(authorization_dict, order_id):
    headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture'.format(order_id=order_id), headers=headers, json={})
    response_dict = json.loads(response.content)
    return response_dict

pp_capture_order = paypal_capture_order(pp_authorization_dict, pp_create_order["id"])

#Show details for authorized payment

def paypal_show_payment(authorization_dict, order_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v2/payments/authorizations/{order_id}'.format(order_id=order_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_payment = paypal_show_payment(pp_authorization_dict, pp_create_order["id"])

#Create batch payout

create_payout_data = {
    "sender_batch_header": {},
    "items": [{
      "recipient_type": "PAYPAL_ID",
      "amount": {
        "value": "12.34",
        "currency": "USD"
      },
      "note": "Thanks for your support!",
      "receiver": "G7MJ5TGUZW8XY"
    },]
}

def paypal_create_payout(authorization_dict, create_payout_data):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payouts', headers=headers, json=create_payout_data)
    response_dict = json.loads(response.content)
    return response_dict

pp_create_payout = paypal_create_payout(pp_authorization_dict, create_payout_data)

#Show payout batch details

def paypal_show_payout(authorization_dict, payout_batch_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/payments/payouts/{payout_batch_id}'.format(payout_batch_id=payout_batch_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_payout = paypal_show_payout(pp_authorization_dict, pp_create_payout["batch_header"]["payout_batch_id"])

#List plans

list_plans_params = {'page_size': '2', 'page': '1', 'total_required': 'true'}

def paypal_list_plans(authorization_dict, list_plans_params):
    headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers, params=list_plans_params)
    response_dict = json.loads(response.content)
    return response_dict

pp_plans_list = paypal_list_plans(pp_authorization_dict, list_plans_params)

#Create plan

create_plan_dict = {
    'product_id': pp_products_list["products"][0]["id"],
    'name': 'test plan',
    'description': 'test_plan',
    'status': 'ACTIVE',
    'billing_cycles': [
        {
            'frequency': {
                'interval_unit': 'MONTH',
                'interval_count': 1,
            },
            'tenure_type': 'REGULAR',
            'sequence': 1,
            'total_cycles': 12,
            'pricing_scheme': {
                'fixed_price': {
                    'value': '11',
                    'currency_code': 'GBP',
                },
            },
        },
    ],
    'payment_preferences': {
        'auto_bill_outstanding': True,
        'setup_fee': {
            'value': '0.0',
            'currency_code': 'GBP',
        },
        'setup_fee_failure_action': 'CANCEL',
        'payment_failure_threshold': 3,
    },
    'taxes': {
        'percentage': '0',
        'inclusive': True,
    },
}

def paypal_create_plan(authorization_dict, create_plan_dict):
    headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers, json=create_plan_dict)
    response_dict = json.loads(response.content)
    return response_dict

pp_create_plan = paypal_create_plan(pp_authorization_dict, create_plan_dict)

#Update plan

update_plan_dict = [
    {
        'op': 'replace',
        'path': '/description',
        'value': 'test update',
    },
    {
        'op': 'replace',
        'path': '/payment_preferences/payment_failure_threshold',
        'value': 3,
    },
    {
        'op': 'replace',
        'path': '/payment_preferences/setup_fee',
        'value': {
            'value': '0.0',
            'currency_code': 'GBP',
        },
    },
]

def paypal_update_plan(authorization_dict, plan_id, update_plan_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.patch('https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}'.format(plan_id=plan_id), headers=headers, json=update_plan_dict)
    if response.status_code == 204:
        return True
    else:
        return False
    #return response

pp_update_plan = paypal_update_plan(pp_authorization_dict, pp_create_plan["id"], update_plan_dict)

#Show plan

def paypal_show_plan(authorization_dict, plan_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}'.format(plan_id=plan_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_plan = paypal_show_plan(pp_authorization_dict, pp_create_plan["id"])

#Activate plan

def paypal_activate_plan(authorization_dict, plan_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}/activate'.format(plan_id=plan_id), headers=headers)
    if response.status_code == 204:
        return True
    else:
        return False
    #return response

pp_activate_plan = paypal_activate_plan(pp_authorization_dict, pp_create_plan["id"])

#Deactivate plan

def paypal_deactivate_plan(authorization_dict, plan_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}/deactivate'.format(plan_id=plan_id), headers=headers)
    if response.status_code == 204:
        return True
    else:
        return False
    #return response

pp_deactivate_plan = paypal_deactivate_plan(pp_authorization_dict, pp_create_plan["id"])

#Update plan pricing

update_plan_pricing_dict = {
    'pricing_schemes': [
        {
            'billing_cycle_sequence': 1,
            'pricing_scheme': {
                'fixed_price': {
                    'value': '50',
                    'currency_code': 'GBP',
                },
            },
        },
    ],
}

def paypal_update_plan_pricing(authorization_dict, plan_id, update_plan_pricing_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}/update-pricing-schemes'.format(plan_id=plan_id), headers=headers, json=update_plan_pricing_dict)
    if response.status_code == 204:
        return True
    else:
        return False
    #return response

pp_update_plan_pricing = paypal_update_plan_pricing(pp_authorization_dict, pp_create_plan["id"], update_plan_pricing_dict)

#Create subscription

create_subscription_dict = {
    'plan_id': pp_create_plan["id"],
    'application_context': {
        'brand_name': 'test subscription label',
        'shipping_preference': 'NO_SHIPPING',
        'user_action': 'SUBSCRIBE_NOW',
        'payment_method': {
            'payer_selected': 'PAYPAL',
            'payee_preferred': 'IMMEDIATE_PAYMENT_REQUIRED',
        },
        'return_url': 'http://127.0.0.1:3000',
        'cancel_url': 'http://127.0.0.1:8000',
    },
}

def paypal_create_subscription(authorization_dict, create_subscription_dict):
    headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions', headers=headers, json=create_subscription_dict)
    response_dict = json.loads(response.content)
    return response_dict

pp_create_subscription = paypal_create_subscription(pp_authorization_dict, create_subscription_dict)

#Show subscription

def paypal_show_subscription(authorization_dict, subscription_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.get('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}'.format(subscription_id=subscription_id), headers=headers)
    response_dict = json.loads(response.content)
    return response_dict

pp_show_subscription = paypal_show_subscription(pp_authorization_dict, pp_create_subscription["id"])

#Activate subscription
#dont need

def paypal_activate_subscription(authorization_dict, subscription_id):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/activate'.format(subscription_id=subscription_id), headers=headers)
    #if response.status_code == 204:
    #    return True
    #else:
    #    return False
    return response

pp_activate_subscription = paypal_activate_subscription(pp_authorization_dict, pp_create_subscription["id"])

#Cancel subscription

cancel_subscription_dict = {"reason": "test reason"}

def paypal_cancel_subscription(authorization_dict, subscription_id, cancel_subscription_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/cancel'.format(subscription_id=subscription_id), headers=headers, json=cancel_subscription_dict)
    if response.status_code == 204:
        return True
    else:
        return False
    return response

pp_cancel_subscription = paypal_cancel_subscription(pp_authorization_dict, pp_create_subscription["id"], cancel_subscription_dict)

#Capture authorized payment on subscription

capture_subscription_dict = {
    "note": "test capture_subscription",
    "capture_type": "OUTSTANDING_BALANCE",
    "amount": {
    "currency_code": "GBP",
    "value": "11.5"
    }
}

def paypal_capture_subscription(authorization_dict, subscription_id, capture_subscription_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/capture'.format(subscription_id=subscription_id), headers=headers, json=capture_subscription_dict)
    #if response.status_code == 202:
    #    return True
    #else:
    #    return False
    return response

pp_capture_subscription = paypal_capture_subscription(pp_authorization_dict, pp_create_subscription["id"], capture_subscription_dict)

#Suspend subscription

suspend_subscription_dict = {"reason": "test reason"}

def paypal_suspend_subscription(authorization_dict, subscription_id, suspend_subscription_dict):
    headers = {'Content-Type': 'application/json', 'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"], access_token=authorization_dict["access_token"])}
    response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/cancel'.format(subscription_id=subscription_id), headers=headers, json=suspend_subscription_dict)
    if response.status_code == 204:
        return True
    else:
        return False
    return response

pp_suspend_subscription = paypal_suspend_subscription(pp_authorization_dict, pp_create_subscription["id"], suspend_subscription_dict)