from django.views.decorators.csrf import csrf_exempt
import ApartmentsApp.apartmentsMethods as apartmentsMethods
import ApartmentsApp.projectsMethods as projectsMethods
import ApartmentsApp.projectAvailabilityMethods as projectAvailabilityMethods
import ApartmentsApp.apartmentStatusMethods as apartmentStatusMethods

from django.http.response import JsonResponse

# Create your views here.

@csrf_exempt
def apartmentsApi(request,id=False, date=False):
    if request.method=='GET':
        if id:
            if date:
                return apartmentsMethods.getApartmentAtDate(id,date)
            return apartmentsMethods.getApartment(id)
        else:
            return apartmentsMethods.getAllApartments()
    elif request.method=='POST':
        return apartmentsMethods.postApartment(request)
    elif request.method=='PUT':
        return apartmentsMethods.putApartment(request)
    elif request.method=='DELETE':
        return apartmentsMethods.deleteApartment(id)

@csrf_exempt
def lastApartmentApi(request):
    if request.method=='GET':
        return apartmentsMethods.getLastApartment()

@csrf_exempt
def projectsApi(request,id=False, date=False):
    if request.method=='GET':
        if id:
            if date:
                return projectsMethods.getProjectAtDate(id,date)
            return projectsMethods.getProject(id)
        else:
            return projectsMethods.getAllProjects()            
    elif request.method=='POST':
        return projectsMethods.postProject(request)
    elif request.method=='PUT':
        return projectsMethods.putProject(request)
    elif request.method=='DELETE':
        return projectsMethods.deleteProject(id)

@csrf_exempt
def lastProjectApi(request):
    if request.method=='GET':
        return projectsMethods.getLastProject()

@csrf_exempt
def projectAvailabilitiesApi(request,id=False, date=False):
    if request.method=='GET':
        if id:
            if date:
                return projectAvailabilityMethods.getProjectAvailabilityAtDate(id,date)
            return projectAvailabilityMethods.getProjectAvailability(id)
        else:
            return projectAvailabilityMethods.getAllProjectAvailability()
            # return JsonResponse(f"Could not get project availability data - missing project ID",safe=False)        
    elif request.method=='POST':
        return projectAvailabilityMethods.postProjectAvailability(request)
    elif request.method=='PUT':
        return projectAvailabilityMethods.putProjectAvailability(request)
    elif request.method=='DELETE':
        return projectAvailabilityMethods.deleteProjectAvailability(id)

@csrf_exempt
def apartmentStatusesApi(request,id=False, date=False):
    if request.method=='GET':
        if id:
            if date:
                return apartmentStatusMethods.getApartmentStatusAtDate(id,date)
            return apartmentStatusMethods.getApartmentStatus(id)
        else:
            return apartmentStatusMethods.getAllApartmentStatus()
            # return JsonResponse(f"Could not get Apartment Status data - missing Apartment ID",safe=False)        
    elif request.method=='POST':
        return apartmentStatusMethods.postApartmentStatus(request)
    elif request.method=='PUT':
        return apartmentStatusMethods.putApartmentStatus(request)
    elif request.method=='DELETE':
        return apartmentStatusMethods.deleteApartmentStatus(id)