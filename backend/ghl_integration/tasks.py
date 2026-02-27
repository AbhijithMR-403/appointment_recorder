import requests
from celery import shared_task
from ghl_integration.models import GHLAuthCredentials
from decouple import config
@shared_task
def make_refresh_token_call():
    credentials = GHLAuthCredentials.objects.all()
    print("credentials token", credentials)
    for credential in credentials:
        refresh_token = credential.refresh_token
        print("refresh_token", refresh_token)

        response = requests.post('https://services.leadconnectorhq.com/oauth/token', data={
            'grant_type': 'refresh_token',
            'client_id': config("GHL_CLIENT_ID"),
            'client_secret': config("GHL_CLIENT_SECRET"),
            'refresh_token': refresh_token
        })
        if response.status_code == 200:
            response_data = response.json()
            print("response is successful")
        else:
            response_data = response.json()
            print("response is not successful")

        print("response_data", response_data)

        obj, created = GHLAuthCredentials.objects.update_or_create(
                location_id= credential.location_id,
                defaults={
                    "access_token": response.json().get("access_token"),
                    "refresh_token": response.json().get("refresh_token"),
                    "expires_in": response.json().get("expires_in"),
                    "scope": response.json().get("scope"),
                    "user_type": response.json().get("userType"),
                    "company_id": response.json().get("companyId")
                }
            )
    