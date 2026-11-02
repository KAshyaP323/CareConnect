from rest_framework import serializers
from clinic.models import DocterDB,AppointmentDB

class Doctor_serializer(serializers.ModelSerializer):
    class Meta:
        model=DocterDB
        fields="__all__"
        read_only_fields=["id"]

class Appointment_serializer(serializers.ModelSerializer):
    class Meta:
        model=AppointmentDB
        fields="__all__"
        read_only_fields=["id"]   

    def validate(self, validated_data):
        phone=validated_data.get("phone")
        Appointment_date=validated_data.get("Appointment_date")
        if AppointmentDB.objects.filter(
            phone=phone,
            Appointment_date=Appointment_date).exists():
            raise serializers.ValidationError("Already Booked")
        else:
            return validated_data