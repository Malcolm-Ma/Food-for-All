from FoodForAll.settings import PAYMENT_CLIENT_ID, PAYMENT_CLIENT_SECRET
import requests
import json
import time

# The code in this script is used to interact with the paypal sandbox interface in order to implement the payment function

payment_authorization = {"token_type": "", "access_token": "", "expires_time": int(time.time()) - 1}

# Payment class
class Payment(object):
    # Function to get authentication information from paypal sandbox
    @staticmethod
    def authorization(client_id=PAYMENT_CLIENT_ID, secret=PAYMENT_CLIENT_SECRET):
        global payment_authorization
        if payment_authorization["expires_time"] < int(time.time()):
            headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
            data = {'grant_type': 'client_credentials'}
            response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data, auth=(client_id, secret))
            response_dict = json.loads(response.content)
            payment_authorization["token_type"] = response_dict["token_type"]
            payment_authorization["access_token"] = response_dict["access_token"]
            payment_authorization["expires_time"] = int(time.time()) + response_dict["expires_in"]
        return payment_authorization

    # Function to request a product ID for a project in the paypal sandbox
    @staticmethod
    def create_product(product_name, product_description, home_url, image_url):
        authorization_dict = Payment.authorization()
        create_dict = {'name': product_name[:127] if len(product_name) >= 1 else "-",
                       'description': product_description[:127] if len(product_description) >= 1 else "-",
                       'type': 'SERVICE',
                       'category': 'CHARITY',
                       'image_url': image_url,
                       'home_url': home_url}
        headers = {'Prefer': 'return=representation',
                   'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers,
                                 json=create_dict)
        response_dict = json.loads(response.content)
        return response_dict

    # Functions for creating an order of project in paypal sandbox
    @staticmethod
    def create_order(currency_type, price, return_url, cancel_url):
        authorization_dict = Payment.authorization()
        order_data = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'currency_code': currency_type,
                        'value': str(price),
                    },
                },
            ],
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "payment_instruction": {
                "platform_fees": [
                    {
                        "amount": {
                            "currency_code": currency_type,
                            "value": "0.00"
                        },
                    }
                ],
            },
        }
        headers = {
            'Prefer': 'return=representation',
            'Content-Type': 'application/json',
            'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                  access_token=authorization_dict["access_token"]),
        }

        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers,
                                 json=order_data)
        response_dict = json.loads(response.content)
        return response_dict

    # Function for collecting and confirming whether an order has been paid or not in the paypal sandbox
    @staticmethod
    def capture_order(order_id):
        authorization_dict = Payment.authorization()
        headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture'.format(order_id=order_id),
            headers=headers, json={})
        response_dict = json.loads(response.content)
        return response_dict

    # Functions for spending money in paypal sandbox
    @staticmethod
    def create_payout(currency_type, price, receiver):
        authorization_dict = Payment.authorization()
        payout_data = {
            "sender_batch_header": {},
            "items": [{
                "recipient_type": "PAYPAL_ID",
                "amount": {
                    "value": str(price),
                    "currency": currency_type
                },
                "note": "Thanks for your support!",
                "receiver": receiver
            }, ]
        }
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payouts', headers=headers,
                                 json=payout_data)
        response_dict = json.loads(response.content)
        return response_dict

    # Function for creating a subscription plan ID for an project in the paypal sandbox
    @staticmethod
    def create_plan(product_id, plan_name, plan_description, currency_type, price):
        authorization_dict = Payment.authorization()
        create_plan_dict = {
            'product_id': product_id,
            'name': plan_name[:127] if len(plan_name) >= 1 else "-",
            'description': plan_description[:127] if len(plan_description) >= 1 else "-",
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
                            'value': str(price),
                            'currency_code': currency_type,
                        },
                    },
                },
            ],
            'payment_preferences': {
                'auto_bill_outstanding': True,
                'setup_fee': {
                    'value': 0.0,
                    'currency_code': currency_type,
                },
                'setup_fee_failure_action': 'CANCEL',
                'payment_failure_threshold': 3,
            },
            'taxes': {
                'percentage': '0',
                'inclusive': True,
            },
        }
        headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers,
                                 json=create_plan_dict)
        response_dict = json.loads(response.content)
        return response_dict

    # Function for activating subscription plan
    @staticmethod
    def activate_plan(plan_id):
        authorization_dict = Payment.authorization()
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}/activate'.format(plan_id=plan_id),
            headers=headers)
        if response.status_code == 204:
            return True
        else:
            return False

    # Function for deactivating subscription plan
    @staticmethod
    def deactivate_plan(plan_id):
        authorization_dict = Payment.authorization()
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/plans/{plan_id}/deactivate'.format(plan_id=plan_id),
            headers=headers)
        if response.status_code == 204:
            return True
        else:
            return False

    # Function for creating subscription plan order in the paypal sandbox
    @staticmethod
    def create_subscription(plan_id, brand_name, return_url, cancel_url):
        authorization_dict = Payment.authorization()
        create_subscription_dict = {
            'plan_id': plan_id,
            'application_context': {
                'brand_name': brand_name[:127] if len(brand_name) >= 1 else "-",
                'shipping_preference': 'NO_SHIPPING',
                'user_action': 'SUBSCRIBE_NOW',
                'payment_method': {
                    'payer_selected': 'PAYPAL',
                    'payee_preferred': 'IMMEDIATE_PAYMENT_REQUIRED',
                },
                'return_url': return_url,
                'cancel_url': cancel_url,
            },
        }
        headers = {'Prefer': 'return=representation', 'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(
                       token_type=authorization_dict["token_type"],
                       access_token=authorization_dict["access_token"])}
        response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/subscriptions', headers=headers,
                                 json=create_subscription_dict)
        response_dict = json.loads(response.content)
        return response_dict

    # Function for getting information of subscription plans
    @staticmethod
    def show_subscription(subscription_id):
        authorization_dict = Payment.authorization()
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.get('https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}'.format(
            subscription_id=subscription_id), headers=headers)
        response_dict = json.loads(response.content)
        return response_dict

    # Function for canceling subscription plan order in the paypal sandbox
    @staticmethod
    def cancel_subscription(subscription_id, reason):
        authorization_dict = Payment.authorization()
        cancel_subscription_dict = {"reason": reason}
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/cancel'.format(
                subscription_id=subscription_id), headers=headers, json=cancel_subscription_dict)
        if response.status_code == 204:
            return True
        else:
            return False

    # Function for suspendding subscription plan order in the paypal sandbox
    @staticmethod
    def suspend_subscription(subscription_id, reason):
        authorization_dict = Payment.authorization()
        suspend_subscription_dict = {"reason": reason}
        headers = {'Content-Type': 'application/json',
                   'Authorization': '{token_type} {access_token}'.format(token_type=authorization_dict["token_type"],
                                                                         access_token=authorization_dict[
                                                                             "access_token"])}
        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/cancel'.format(
                subscription_id=subscription_id), headers=headers, json=suspend_subscription_dict)
        if response.status_code == 204:
            return True
        else:
            return False