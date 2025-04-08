try:
    import requests
except:
    pass
import hashlib
import base64
import json
import uuid


class Cryptomus:
    def __init__(self, api_key, merchant_id ):
        'Initialises the Cryptomus python API client. pass the api_key first, then merchant_id next.'
        self.api_key = api_key
        self.merchant_id = merchant_id

    def charge(self, payload):
        """
        This method will attempt to charge a customer, basing on the payload you pass as a param to it. The charge endpoint is: https://api.cryptomus.com/v1/payment

        Visit the official Cryptomus API documentation to see how the payload should look like
        
        """
        sign, payload_json = encrypt_us(payload, api_key=self.api_key)
        endpoint_url = "https://api.cryptomus.com/v1/payment"

        headers = {
            "merchant": self.merchant_id,
            "sign": sign,
            "Content-Type": "application/json"
        }

        res = requests.post(endpoint_url, headers=headers, data=payload_json)
        return res
    
    def verify_charge(self, data):
        'Verifies the signature from the webhook response to ensure no faked signs. Pass the the json parsed response as a param | This method returns a json with  verified=True if verified and the signature from the webhook'
        is_verified = False
        received_sign = data.pop("sign", None)

        if not received_sign:
            jres = make_response(is_verified, received_sign)
            return jres

        processed_data = base64.b64encode(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        generated_hash = hashlib.md5((processed_data.decode() + self.api_key).encode()).hexdigest()
       
        if not constant_time_compare(generated_hash, received_sign):
            jres = make_response(is_verified, received_sign)
            return jres

        else:
            is_verified = True
            jres = make_response(is_verified, received_sign)
            return jres


def make_response(is_verified, received_sign):
        jr = {
            "verified": is_verified,
            "received_sign": received_sign
        }
        jres = json.dumps(jr)

        return jres

def constant_time_compare(val1, val2):
    """
    Return True if the two strings are equal, False otherwise.
    The time taken is independent of the number of characters that match.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0
def encrypt_us(payload, api_key):
    payload_json = json.dumps(payload)

    # Base64 encode payload
    payload_base64 = base64.b64encode(payload_json.encode()).decode()
    sign_data = payload_base64 + api_key
    sign = hashlib.md5(sign_data.encode()).hexdigest()

    return sign, payload_json 