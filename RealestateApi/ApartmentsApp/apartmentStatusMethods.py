from ApartmentsApp.models import ApartmentStatus
from ApartmentsApp.serializers import ApartmentStatusSerializer

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from django.db.models.base import ObjectDoesNotExist

def getAllApartmentStatus():
    apartment_status = ApartmentStatus.objects.all()
    apartment_status_serializer=ApartmentStatusSerializer(apartment_status,many=True)
    return JsonResponse(apartment_status_serializer.data,safe=False)

def getApartmentStatus(id):
    try:
        apartment_status = ApartmentStatus.objects.filter(Apartment=id)
        apartment_status_serializer=ApartmentStatusSerializer(apartment_status, many=True)
        return JsonResponse(apartment_status_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve apartment with id = {id}",safe=False)

def getApartmentStatusAtDate(id,date):
    try:
        apartment_status = ApartmentStatus.objects.get(Apartment=id, ScrapingDate=date)
        apartment_status_serializer=ApartmentStatusSerializer(apartment_status)
        return JsonResponse(apartment_status_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve apartment with id = {id} on date = {date}",safe=False)

def postApartmentStatus(request):
    apartment_status_data=JSONParser().parse(request)
    try:
        ApartmentStatus.objects.get(Apartment=apartment_status_data['Apartment'], ScrapingDate=apartment_status_data['ScrapingDate'])
        return JsonResponse("Failed to add - item already exists",safe=False)
    except ObjectDoesNotExist as odne: 
        apartment_status_serializer=ApartmentStatusSerializer(data=apartment_status_data)
        if apartment_status_serializer.is_valid():
            apartment_status_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
    return JsonResponse("Failed to add",safe=False)

def putApartmentStatus(request):
    apartment_status_data=JSONParser().parse(request)
    try:
        apartment_status=ApartmentStatus.objects.get(Apartment=apartment_status_data['Apartment'], ScrapingDate=apartment_status_data['ScrapingDate'])
        apartment_status_serializer=ApartmentStatusSerializer(apartment_status,data=apartment_status_data)
        if apartment_status_serializer.is_valid():
            apartment_status_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse("Failed to update - item does not exist in database", safe=False)
    return JsonResponse("Failed to Update", safe=False)

def deleteApartmentStatus(id):
    try:
        apartment=ApartmentStatus.objects.get(AvailibilityID=id)
        apartment.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to delete apartment status with id = {id}",safe=False)