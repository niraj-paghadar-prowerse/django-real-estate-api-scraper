from rest_framework import serializers
from ApartmentsApp.models import ApartmentStatus, Apartments, ProjectAvailability, Projects

class ProjectAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectAvailability
        fields=( 'AvailibilityID', 'Project', 'ProjectAvailableApartments', 'ScrapingDate')
'''
class ProjectAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Projects
        fields=( 'ProjectID', 'ProjectName', 'ProjectAddress', 'ProjectTotalApartments', 'ScrapingDate', 'HistoricalAvailabilities')'''

'''class ApartmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApartmentStatus
        fields=('ApartmentId', 'ApartmentName', 'ApartmentAddress', 'NumberOfRooms', 'AppartmentFloor', 'ApartmentSize', 'TotalAreaSize', 'BalconySize', 'ScrapingDate', 'HistoricalStatuses')'''
    
class ApartmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApartmentStatus
        fields=('StatusID', 'Apartment','ReservationStatus','SalesPrice','ScrapingDate')

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Apartments
        fields=('ApartmentID', 'ApartmentName', 'ApartmentAddress', 'NumberOfRooms', 'AppartmentFloor', 'ApartmentSize', 'TotalAreaSize', 'BalconySize', 'ScrapingDate', 'Project')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Projects
        fields=( 'ProjectID', 'ProjectName', 'ProjectAddress', 'ProjectTotalApartments', 'ScrapingDate')

