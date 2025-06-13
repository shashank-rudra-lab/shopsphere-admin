# auth_helper.py
from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import id_token

# Audience = your API Gateway URL
API_GATEWAY_AUDIENCE = 'https://shopsphere-gateway-46h5n97t.uc.gateway.dev'

def get_service_account_token():
    # Get default credentials (Cloud Run provides them)
    credentials, _ = default()

    # Use the default credentials to get an Identity Token
    request = Request()
    target_audience = API_GATEWAY_AUDIENCE
    token = id_token.fetch_id_token(request, target_audience)

    return token
