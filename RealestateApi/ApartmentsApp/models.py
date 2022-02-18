from django.db import models
from datetime import datetime

from django.db.models.fields import related    

# Create your models here.
    
class Projects(models.Model):
    ProjectID = models.AutoField(primary_key=True)
    ProjectName = models.CharField(max_length=100)
    ProjectAddress = models.CharField(max_length=100)
    ProjectTotalApartments =  models.IntegerField(null=True, blank=True)
    ScrapingDate = models.DateField(default=datetime.now)       

class ProjectAvailability(models.Model):
    AvailibilityID= models.AutoField(primary_key=True)
    Project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='HistoricalAvailabilities') 
    ProjectAvailableApartments =  models.IntegerField(null=True, blank=True)
    ScrapingDate = models.DateField(default=datetime.now)  

class Apartments(models.Model):
    ApartmentID = models.AutoField(primary_key=True)
    ApartmentName = models.CharField(max_length=100)
    ApartmentAddress = models.CharField(max_length=100)
    NumberOfRooms = models.IntegerField(null=True, blank=True)
    AppartmentFloor = models.CharField(max_length=20, null=True, blank=True)
    ApartmentSize =  models.FloatField(null=True, blank=True)
    TotalAreaSize =  models.FloatField(null=True, blank=True)
    BalconySize =  models.FloatField(null=True, blank=True)
    Project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True) 
    ScrapingDate = models.DateField(default=datetime.now)

class ApartmentStatus(models.Model):
    StatusID = models.AutoField(primary_key=True)
    Apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE, related_name='HistoricalStatuses') 
    ReservationStatus = models.CharField(max_length=100, null=True, blank=True)
    SalesPrice =  models.FloatField(null=True, blank=True)
    ScrapingDate = models.DateField(default=datetime.now)
