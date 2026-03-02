import requests


def add_contact_note(contact_id: str, body: str, access_token: str) -> dict:
    """
    Add a note to a contact via GoHighLevel API.

    Args:
        contact_id: The GHL contact ID.
        body: The note text.
        access_token: Bearer token for authentication.

    Returns:
        dict: API response (typically the created note).

    Raises:
        requests.HTTPError: On non-2xx response.
    """
    url = f"https://services.leadconnectorhq.com/contacts/{contact_id}/notes"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28",
    }
    payload = {"body": body}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def get_location_name(location_id: str, access_token: str) -> str:
    url = f"https://services.leadconnectorhq.com/locations/{location_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-07-28"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for HTTP errors

    data = response.json()
    return data