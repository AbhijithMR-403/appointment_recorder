from django.utils.dateparse import parse_datetime
from ghl_integration.models import Contact

def create_or_update_contact(data):
    contact_id = data.get("id")
    date_added = parse_datetime(data.get("dateAdded")) if data.get("dateAdded") else None
    contact, created = Contact.objects.update_or_create(
        contact_id=contact_id,
        defaults={
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "dnd": data.get("dnd", False),
            "country": data.get("country"),
            "date_added": date_added,
            "location_id": data.get("locationId"),
        }
    )
    print("Contact created/updated:", contact_id)

def delete_contact(data):
    contact_id = data.get("id")
    try:
        contact = Contact.objects.get(contact_id=contact_id)
        contact.delete()
        print("Contact deleted:", contact_id)
    except Contact.DoesNotExist:
        print("Contact not found for deletion:", contact_id)


