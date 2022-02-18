from ApartmentsApp.models import ProjectAvailability
from ApartmentsApp.serializers import ProjectAvailabilitySerializer

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from django.db.models.base import ObjectDoesNotExist



def getAllProjectAvailability():
    project_availability = ProjectAvailability.objects.all()
    project_availability_serializer=ProjectAvailabilitySerializer(project_availability,many=True)
    return JsonResponse(project_availability_serializer.data,safe=False)

def getProjectAvailability(id):
    try:
        project_availability = ProjectAvailability.objects.filter(Project=id)
        project_availability_serializer=ProjectAvailabilitySerializer(project_availability, many=True)
        return JsonResponse(project_availability_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve project with id = {id}",safe=False)

def getProjectAvailabilityAtDate(id,date):
    try:
        project_availability = ProjectAvailability.objects.get(Project=id, ScrapingDate=date)
        project_availability_serializer=ProjectAvailabilitySerializer(project_availability)
        return JsonResponse(project_availability_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve project with id = {id} on date = {date}",safe=False)

def postProjectAvailability(request):
    project_availability_data=JSONParser().parse(request)
    try:
        ProjectAvailability.objects.get(Project=project_availability_data['Project'], ScrapingDate=project_availability_data['ScrapingDate'])
        return JsonResponse("Failed to add - item already exists",safe=False)
    except ObjectDoesNotExist as odne: 
        project_availability_serializer=ProjectAvailabilitySerializer(data=project_availability_data)
        if project_availability_serializer.is_valid():
            project_availability_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
    return JsonResponse("Failed to add",safe=False)

def putProjectAvailability(request):
    project_availability_data=JSONParser().parse(request)
    try:
        project_availability=ProjectAvailability.objects.get(Project=project_availability_data['Project'], ScrapingDate=project_availability_data['ScrapingDate'])
        project_availability_serializer=ProjectAvailabilitySerializer(project_availability,data=project_availability_data)
        if project_availability_serializer.is_valid():
            project_availability_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse("Failed to update - item does not exist in database", safe=False)
    return JsonResponse("Failed to Update", safe=False)

def deleteProjectAvailability(id):
    try:
        project=ProjectAvailability.objects.get(AvailibilityID=id)
        project.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to delete project availability with id = {id}",safe=False)