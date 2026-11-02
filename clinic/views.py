from django.shortcuts import render,get_object_or_404
from clinic.serializers import Doctor_serializer,Appointment_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DocterDB,AppointmentDB
from datetime import datetime,time,timedelta
from rest_framework import serializers

# Create your views here.
class DocterListCreateView(APIView):
    def get(self, request):
        qs=DocterDB.objects.all()
        serializer_instance=Doctor_serializer(qs, many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=Doctor_serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class DoctorRetriveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs=get_object_or_404(DocterDB, id=pk)
        serializer_instance=Doctor_serializer(qs)
        return Response(serializer_instance.data)

    def put(self, request, pk):
        form_data=request.data
        doctor_object=get_object_or_404(DocterDB, id=pk)
        serializer_instance=Doctor_serializer(data=form_data, instance=doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self, request, pk):
        doctor_object=get_object_or_404(DocterDB, id=pk)
        doctor_object.delete()
        return Response(data={"Message":"Deleted.."})        

class AppointmentListCreateView(APIView):
    def get(self, request):
        qs=AppointmentDB.objects.all()
        serializer_instance=Appointment_serializer(qs, many=True)
        return Response(serializer_instance.data)

    def post(self, request):
        form_data=request.data
        serializer_instance=Appointment_serializer(data=form_data)
        if serializer_instance.is_valid():
            Appointment_date=serializer_instance.validated_data.get("Appointment_date")
            doctor_id=serializer_instance.validated_data.get("doctor_id")
            last_appointment=AppointmentDB.objects.filter(Appointment_date=Appointment_date,
                                                          doctor_id=doctor_id
                                                          ).order_by("-token_number").first()
            if last_appointment is None:
                form_data["token_number"]=1
                form_data["Appointment_time"]=time(10,0)
            else:
                form_data["token_number"]=last_appointment.token_number+1
                currunt_time=datetime.combine(Appointment_date, last_appointment.Appointment_time)
                next_time=currunt_time+timedelta(minutes=15)  
                #LUNCH
                if next_time.time()==time(12, 30):
                    next_time=datetime.combine(Appointment_date, time(13,30))
                form_data["Appointment_time"]=next_time
                #SLOT COMPLETION
                if next_time.time()==time(17, 30):
                    raise serializers.ValidationError("No slot available..")
            qs=AppointmentDB.objects.create(**form_data)
            serializer_instance=Appointment_serializer(qs)
            return Response(data={
                "Status":"BookedcSuccessfully..",
                "Token Number": form_data["token_number"],
                "Appointment Time": form_data["Appointment_time"]
            })
        else:
            return Response(data=serializer_instance.errors)       