from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "contact_id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "dnd",
            "country",
            "date_added",
            "location_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
