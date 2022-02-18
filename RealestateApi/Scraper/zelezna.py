import requests
from time import sleep
from datetime import datetime
import lxml.html
import pandas as pd


def findApartmentInDB(apartment):
    url = 'http://127.0.0.1:8000/apartments'
    db_apartments = requests.get(url).json()
    for db_apartment in db_apartments:
        if db_apartment['ApartmentName'] == apartment['ApartmentName']:
            return db_apartment
    return None

def getLastApartmentInDB():
    url = 'http://127.0.0.1:8000/apartment/last'
    db_apartment = requests.get(url).json()
    return db_apartment

def findTodaysStatus(apartment):
    apartment_id = apartment["ApartmentID"]
    today = datetime.today().strftime('%Y-%m-%d')
    url = f'http://127.0.0.1:8000/status/{apartment_id}/{today}'
    response = requests.get(url)
    if(response.status_code == 200):
        db_status = response.json()
        return db_status
    return None

def findProjectID(project_name):
    url = 'http://127.0.0.1:8000/projects'
    db_projects = requests.get(url).json()
    for db_project in db_projects:
        if db_project['ProjectName'] == project_name:
            return db_project['ProjectID']
    return -1

def getLastProjectInDB():
    url = 'http://127.0.0.1:8000/project/last'
    db_project = requests.get(url).json()
    return db_project

def findProjectInDBByName(project_name):
    url = 'http://127.0.0.1:8000/projects'
    db_projects = requests.get(url).json()
    for db_project in db_projects:
        if db_project['ProjectName'] == project_name:
            return db_project
    return None

def findTodaysAvailability(project):
    project_id = project["ProjectID"]
    today = datetime.today().strftime('%Y-%m-%d')
    url = f'http://127.0.0.1:8000/availability/{project_id}/{today}'
    response = requests.get(url)
    if(response.status_code == 200):
        db_availability = response.json()
        return db_availability
    return None


def scrapeZelezna():
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    url = 'https://zelezna.sk/ponuka-bytov/'
    res = requests.get(url, headers=headers)

    tree = lxml.html.fromstring(res.text)
    links = tree.xpath('//div[@class="work-item style-5"]/a/@href')

    apartment_data = []

    scrapingDate = datetime.today().strftime('%Y-%m-%d')
    availableApartmentsCounter = 0

    for link in links:

        dict = {

        "ApartmentName": None,
        "ApartmentAddress": "K Železnej studienke 7, 9, 11  ",
        "NumberOfRooms": None,
        "AppartmentFloor" : None,
        "ApartmentSize": None,
        "TotalAreaSize": None,
        "BalconySize" : None,
        "ReservationStatus": None,
        "SalesPrice": None,
        "ScrapingDate": scrapingDate,
        "ProjectName": 'Rezidencia K Železnej Studienke',
    }

        sleep(2)

        res = requests.get(link, headers=headers)
        tree = lxml.html.fromstring(res.text)

        print(f"Getting link {link}")
        print(res)

        try:
            appName = tree.xpath('(//div[@class="wpb_wrapper"]/h2)[1]/text()')[0].strip()
            if not appName == '':
                dict["ApartmentName"] =  appName
        except IndexError:
            pass

        try:
            numberOfRooms = tree.xpath('//div[@class="nectar-fancy-ul"]//ul/li[1]/strong/following-sibling::text()')[0].strip().replace('–', '')
            if not numberOfRooms == '':
                dict["NumberOfRooms"] =  int(numberOfRooms)
        except IndexError:
            pass

        try:
            apartmentFloor =  tree.xpath('//div[@class="nectar-fancy-ul"]//ul/li[2]/strong/following-sibling::text()')[0].strip().replace('–', '')
            if not apartmentFloor == '':
                dict["AppartmentFloor"] =  apartmentFloor
        except IndexError:
            pass

        try:
            apartmentSize =  tree.xpath('//div[@class="nectar-fancy-ul"]//ul/li[3]/strong/following-sibling::text()')[0].strip().replace(',','.').replace('–', '')
            if not apartmentSize == '':
                dict["ApartmentSize"] =  float(apartmentSize)

        except IndexError:
            pass

        try:
            totalAreaSize =  tree.xpath('//div[@class="nectar-fancy-ul"]//ul/li[5]/strong/following-sibling::text()')[0].strip().replace(',','.').replace('–', '')
            if not totalAreaSize == '':
                dict["TotalAreaSize"] =  float(totalAreaSize)

        except IndexError:
            pass

        try:
            balconySize =  tree.xpath('//div[@class="nectar-fancy-ul"]//ul/li[4]/strong/following-sibling::text()')[0].strip().replace(',','.').replace('–', '')
            if not balconySize == '':
                dict["BalconySize"] =  float(balconySize)

        except IndexError:
            pass

        try:
            dict["ReservationStatus"] =  tree.xpath('(//div[@class="wpb_wrapper"])[4]/h3/span/text()')[0].strip().replace('–', '')
            if dict["ReservationStatus"] == 'Voľný':
                availableApartmentsCounter += 1
        except IndexError:
            pass

        try:
            salesPrice =  tree.xpath('(//div[@class="wpb_wrapper"])[5]/h3/span/text()')[0].strip().replace(' €', '').replace(',','.').replace(' ', '').replace('–', '')

            if not salesPrice == '':
                dict["SalesPrice"] =  float(salesPrice)

        except IndexError:
            pass
        
        apartment_data.append(dict)
    
    postApartmentUrl = 'http://127.0.0.1:8000/apartments'
    statusUrl = 'http://127.0.0.1:8000/status'
    postProjectUrl = 'http://127.0.0.1:8000/projects'
    availabilityUrl = 'http://127.0.0.1:8000/availability'

    db_project = findProjectInDBByName('Rezidencia K Železnej Studienke') 
    if db_project != None: #if the project is already in the db
        db_projectAvailability = findTodaysAvailability(db_project)
        if db_projectAvailability != None: #if there is a availability for today in db - update its values
            updated_availability={
                'Project': db_project['ProjectID'],
                'ProjectAvailableApartments': availableApartmentsCounter,
                'ScrapingDate': scrapingDate          
            }
            response = requests.put(availabilityUrl, json = updated_availability)
            if(response.status_code == 200):
                print(f"Successfully updated availability for project: Rezidencia K Železnej Studienke")
            else:
                print(f"Failed to update availability for project: Rezidencia K Železnej Studienke")
        else: #if there is no availability in the db for today
            availability={
                'Project': db_project['ProjectID'],
                'ProjectAvailableApartments': availableApartmentsCounter,
                'ScrapingDate': scrapingDate     
            }
            response = requests.post(availabilityUrl, json = availability)
            if(response.status_code == 200):
                print(f"Successfully input todays availability for project: Rezidencia K Železnej Studienke")
            else:
                print(f"Failed to input todays availability for project: Rezidencia K Železnej Studienke")
    else:
        projectData = {
            "ProjectName": 'Rezidencia K Železnej Studienke',
            "ProjectAddress": 'Bratislava I | K Železnej Studienke 7, 9, 11, 82, 81104 Bratislava',
            "ProjectTotalApartments": 33,
            "ScrapingDate": scrapingDate
        }
        response = requests.post(postProjectUrl, json = projectData)
        if(response.status_code == 200):
            last_project = getLastProjectInDB()
            availability={
                'Project': last_project['ProjectID'],
                'ProjectAvailableApartments': availableApartmentsCounter,
                'ScrapingDate': scrapingDate
            }
            response = requests.post(availabilityUrl, json = availability)
            if(response.status_code == 200):
                print(f"Successfully input project: Rezidencia K Železnej Studienke, and accompanying availability")
            else:
                print(f"Successfully input project: Rezidencia K Železnej Studienke, but NOT the availability")
        else:
            print(f"Failed to imput project: Rezidencia K Železnej Studienke")
    
    for apartment in apartment_data:
        db_apartment = findApartmentInDB(apartment) 
        if db_apartment != None: #if the apartment is alreadI y in the db
            db_apartmentStatus = findTodaysStatus(db_apartment)
            if db_apartmentStatus != None: #if there is a status for today in db - update its values
                updated_status={
                    'Apartment': db_apartment['ApartmentID'],
                    'ReservationStatus': apartment['ReservationStatus'],
                    'SalesPrice': apartment['SalesPrice'],
                    'ScrapingDate': apartment['ScrapingDate'],           
                }
                response = requests.put(statusUrl, json = updated_status)
                if(response.status_code == 200):
                    print(f"Successfully updated status for apartment: {db_apartment['ApartmentName']}")
                else:
                    print(f"Failed to update status for apartment: {apartment['ApartmentName']}")
            else: #if there is no status in the db for today
                status={
                    'Apartment': db_apartment['ApartmentID'],
                    'ReservationStatus': apartment['ReservationStatus'],
                    'SalesPrice': apartment['SalesPrice'],
                    'ScrapingDate': apartment['ScrapingDate'],           
                }
                response = requests.post(statusUrl, json = status)
                if(response.status_code == 200):
                    print(f"Successfully input todays status for apartment: {db_apartment['ApartmentName']}")
                else:
                    print(f"Failed to input todays status for apartment: {apartment['ApartmentName']}")
        else: #if the apartment is not yet in the db
            apartmentData = {
                'ApartmentName': apartment['ApartmentName'],
                'ApartmentAddress': apartment['ApartmentAddress'],
                'NumberOfRooms': apartment['NumberOfRooms'],
                'AppartmentFloor': apartment['AppartmentFloor'],
                'ApartmentSize': apartment['ApartmentSize'],
                'TotalAreaSize': apartment['TotalAreaSize'],
                'BalconySize': apartment['BalconySize'],
                'ScrapingDate': apartment['ScrapingDate'],
                'Project': findProjectID(apartment['ProjectName'])
            }
            response = requests.post(postApartmentUrl, json = apartmentData)
            if(response.status_code == 200):
                last_apartment = getLastApartmentInDB()
                status={
                    'Apartment': last_apartment['ApartmentID'],
                    'ReservationStatus': apartment['ReservationStatus'],
                    'SalesPrice': apartment['SalesPrice'],
                    'ScrapingDate': apartment['ScrapingDate']
                }
                response = requests.post(statusUrl, json = status)
                if(response.status_code == 200):
                    print(f"Successfully input apartment: {apartment['ApartmentName']}, and accompanying status")
                else:
                    print(f"Successfully input apartment: {apartment['ApartmentName']}, but NOT the status")
            else:
                print(f"Failed to imput apartment: {apartment['ApartmentName']}")