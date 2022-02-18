from ApartmentsApp.models import Apartments
from ApartmentsApp.serializers import ApartmentSerializer

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from django.db.models.base import ObjectDoesNotExist

    
def getApartment(id):
    try:
        apartment=Apartments.objects.get(ApartmentID=id)
        apartments_serializer=ApartmentSerializer(apartment)
        return JsonResponse(apartments_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve project with id = {id}",safe=False)

def getLastApartment():
    try:
        apartment = Apartments.objects.latest('ApartmentID')
        apartments_serializer=ApartmentSerializer(apartment)
        return JsonResponse(apartments_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve last apartment",safe=False)

def getAllApartments():
    apartments = Apartments.objects.all()
    apartments_serializer=ApartmentSerializer(apartments,many=True)
    return JsonResponse(apartments_serializer.data,safe=False)

def postApartment(request):
    apartment_data=JSONParser().parse(request)
    apartments_serializer=ApartmentSerializer(data=apartment_data)
    print(apartments_serializer)
    if apartments_serializer.is_valid():
        apartments_serializer.save()
        return JsonResponse("Added Successfully",safe=False)
    return JsonResponse("Failed to Add",safe=False)

def putApartment(request):
    apartment_data=JSONParser().parse(request)
    apartment=Apartments.objects.get(ApartmentID=apartment_data['ApartmentID'])
    apartments_serializer=ApartmentSerializer(apartment,data=apartment_data)
    if apartments_serializer.is_valid():
        apartments_serializer.save()
        return JsonResponse("Updated Successfully",safe=False)
    return JsonResponse("Failed to Update")

def deleteApartment(id):
    try:
        apartment=Apartments.objects.get(ApartmentID=id)
        apartment.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to delete apartment with id = {id}",safe=False)