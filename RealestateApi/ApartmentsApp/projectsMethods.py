from ApartmentsApp.models import Projects
from ApartmentsApp.serializers import ProjectSerializer, ProjectAvailabilitySerializer

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from django.db.models.base import ObjectDoesNotExist
  
    
def getProject(id):
    try:
        project=Projects.objects.get(ProjectID=id)
        projects_serializer=ProjectSerializer(project)
        return JsonResponse(projects_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve project with id = {id}",safe=False)

def getProjectAtDate(id,date):
    try:
        project = Projects.objects.get(ProjectID=id, ScrapingDate=date)
        project_serializer=ProjectSerializer(project)
        return JsonResponse(project_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve project with id = {id} on date = {date}",safe=False)

def getLastProject():
    try:
        project = Projects.objects.latest('ProjectID')
        project_serializer=ProjectSerializer(project)
        return JsonResponse(project_serializer.data,safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to retrieve last project",safe=False)

def getAllProjects():
    projects = Projects.objects.all()
    projects_serializer=ProjectSerializer(projects,many=True)
    return JsonResponse(projects_serializer.data,safe=False)

def postProject(request):
    project_data=JSONParser().parse(request)
    projects_serializer=ProjectSerializer(data=project_data)
    if projects_serializer.is_valid():
        projects_serializer.save()
        return JsonResponse("Added Successfully",safe=False)
    return JsonResponse("Failed to Add",safe=False)

def putProject(request):
    project_data=JSONParser().parse(request)
    project=Projects.objects.get(ProjectID=project_data['ProjectID'])
    projects_serializer=ProjectSerializer(project,data=project_data)
    if projects_serializer.is_valid():
        projects_serializer.save()
        return JsonResponse("Updated Successfully",safe=False)
    return JsonResponse("Failed to Update")

def deleteProject(id):
    try:
        project=Projects.objects.get(ProjectID=id)
        project.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    except ObjectDoesNotExist as odne:
        return JsonResponse(f"Failed to delete project with id = {id}",safe=False)