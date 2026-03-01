import json
from decouple import config
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ghl_integration.tasks import fetch_all_contacts_task, handle_webhook_event
from .models import GHLAuthCredentials, WebhookLog, Contact
from .serializers import ContactSerializer
import logging
from ghl_integration import services



logger = logging.getLogger(__name__)


GHL_CLIENT_ID = config("GHL_CLIENT_ID")
GHL_CLIENT_SECRET = config("GHL_CLIENT_SECRET")
GHL_REDIRECTED_URI = config("GHL_REDIRECTED_URI")

TOKEN_URL = "https://services.leadconnectorhq.com/oauth/token"
SCOPE = config("SCOPE")
GHL_VERSION_ID = config("GHL_VERSION_ID",default="")
def auth_connect(request):
    auth_url = ("https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&"
                f"redirect_uri={GHL_REDIRECTED_URI}&"
                f"client_id={GHL_CLIENT_ID}&"
                f"scope={SCOPE}"
                f"{f'&version_id={GHL_VERSION_ID}' if GHL_VERSION_ID else ''}"
                )
    return redirect(auth_url)



def callback(request):
    
    code = request.GET.get('code')
    print(code)

    if not code:
        return JsonResponse({"error": "Authorization code not received from OAuth"}, status=400)

    return redirect(f'{config("BASE_URL")}/api/ghl_integration/auth/tokens?code={code}')


def tokens(request):
    authorization_code = request.GET.get("code")

    if not authorization_code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    data = {
        "grant_type": "authorization_code",
        "client_id": GHL_CLIENT_ID,
        "client_secret": GHL_CLIENT_SECRET,
        "redirect_uri": GHL_REDIRECTED_URI,
        "code": authorization_code,
    }

    response = requests.post(TOKEN_URL, data=data)

    try:
        response_data = response.json()
        if not response_data:
            return JsonResponse({
                "error": "Invalid or empty response from token API",
                "status_code": response.status_code,
            }, status=502)

        data = services.get_location_name(location_id=response_data.get("locationId"), access_token=response_data.get('access_token'))
        location_data = data.get("location")


        obj, created = GHLAuthCredentials.objects.update_or_create(
            location_id= response_data.get("locationId"),
            defaults={
                "access_token": response_data.get("access_token"),
                "refresh_token": response_data.get("refresh_token"),
                "expires_in": response_data.get("expires_in"),
                "scope": response_data.get("scope"),
                "user_type": response_data.get("userType"),
                "company_id": response_data.get("companyId"),
                "user_id":response_data.get("userId"),
                "location_name":location_data.get("name"),
                "timezone": location_data.get("timezone"),
                "business_email":location_data.get("email"),
                "business_phone":location_data.get("phone")
            }
        )
        fetch_all_contacts_task.delay(response_data.get("locationId"), response_data.get("access_token"))

    
        location_id = response_data.get("locationId")
        access_token = response_data.get("access_token")
        
        return JsonResponse({
            "message": "Authentication successful",
            "access_token": response_data.get('access_token'),
            "refresh_token": response_data.get('refresh_token'),
            "token_stored": True
        })
        
    except requests.exceptions.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON response from API",
            "status_code": response.status_code,
            "response_text": response.text[:500]
        }, status=500)
    

@csrf_exempt
def webhook_handler(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        WebhookLog.objects.create(data=data)
        event_type = data.get("type")
        handle_webhook_event.delay(data, event_type)
        return JsonResponse({"message":"Webhook received"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


class ContactListView(APIView):
    """
    GET: List contacts with optional filters.
    Query params:
        - location_id: filter by location ID
        - name: search in first name and last name (case-insensitive partial match)
    """

    def get(self, request):
        queryset = Contact.objects.all().order_by("-date_added", "-created_at")

        location_id = request.query_params.get("location_id", "").strip()
        if location_id:
            queryset = queryset.filter(location_id=location_id)

        name = request.query_params.get("name", "").strip()
        contact_id = request.query_params.get("contact_id", "").strip()
        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        serializer = ContactSerializer(queryset, many=True)
        return Response(
            {"count": queryset.count(), "contacts": serializer.data},
            status=status.HTTP_200_OK,
        )
    