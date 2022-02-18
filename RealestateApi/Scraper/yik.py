import requests
import json
import pandas as pd
from datetime import datetime
import json


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

def findProjectInDB(project):
    url = 'http://127.0.0.1:8000/projects'
    db_projects = requests.get(url).json()
    for db_project in db_projects:
        if db_project['ProjectName'] == project['ProjectName']:
            return db_project
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

def findTodaysAvailability(project):
    project_id = project["ProjectID"]
    today = datetime.today().strftime('%Y-%m-%d')
    url = f'http://127.0.0.1:8000/availability/{project_id}/{today}'
    response = requests.get(url)
    if(response.status_code == 200):
        db_availability = response.json()
        return db_availability
    return None


def scrapeYik():
    payload = {
        "PageSize": 4,
        "StartPage": 0,
        "QueryString": "*",
        "UILanguage": "sk",
        "PageId": 21747,
        "BlockId": 0,
        "SiteId": "yit.sk",
        "Attrs": [
            "inap"
        ],
        "Fields": None,
        "CacheMaxAge": 0,
        "Filter": {
            "Field": "Locale",
            "Value": "sk",
            "Operator": "Equals",
            "AndConditions": [
                {
                    "Field": "ProjectPublish",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "IsAvailable",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "ProductItemForSale",
                    "Value": True,
                    "Operator": "Equals",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "AreaIds",
                    "Value": "cityv62u-q27j-49ue-j59q86mus34t",
                    "Operator": "Any",
                    "AndConditions": [],
                    "OrConditions": []
                },
                {
                    "Field": "BuildingTypeKey",
                    "Value": [
                        "BlockOfFlats",
                        "SemiDetachedHouse",
                        "DetachedHouse",
                        ""
                    ],
                    "Operator": "In",
                    "AndConditions": [],
                    "OrConditions": []
                }
            ],
            "OrConditions": []
        },
        "Facet": [],
        "Order": [
            {
                "Field": "ReservationStatusIndex"
            },
            {
                "Field": "CrmId"
            }
        ]
    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'content-type': 'application/json; charset=utf-8',
    'cookie': "TiPMix=23.5764657257015; x-ms-routing-name=self; ARRAffinity=9e6938bdd5273ac834b9c96b3a02aa5822bd44d7825a58ea9ec27f776457eeff; ARRAffinitySameSite=9e6938bdd5273ac834b9c96b3a02aa5822bd44d7825a58ea9ec27f776457eeff; ASP.NET_SessionId=d0ijxpchepzanwvjg5hi1qhp; EPi_NumberOfVisits=1,2021-12-02T22:39:23; YIT-SessionId=2021120222392360.d0ij1qhp; .EPiForm_BID=a2e30ef7-26b7-48a7-a874-d24ac00cf488; .EPiForm_VisitorIdentifier=a2e30ef7-26b7-48a7-a874-d24ac00cf488:; CookieConsent={stamp:'3gDDKMuxwN/W6C3JGGrP9gR3EIHola272oSJhE/eKTp9lgucAilPWA==',necessary:true,preferences:true,statistics:true,marketing:true,ver:2,utc:1638484769533,iab2:'CPQnO9QPQnO9QCGABBENBtCsAP_AAH_AAAAAIOtf_X__bX9j-_59f_t0eY1P9_r_v-Qzjhfdt-8F2L_W_L0X42E7NF36pq4KuR4Eu3LBIQNlHMHUTUmwaokVrzHsak2MryNKJ7LEmnMZO2dYGHtPn91TuZKY7_78__fz3z-v_t_-39T37-3_3__5_X---_e_V399zLv9____39nN___9v-CDYBJhqXkAXYljgybRpVCiBGFYSHQCgAooBhaJrABgcFOysAj1BCwAQmoCMCIEGIKMGAQACAQBIREBIAWCARAEQCAAEAKkBCAAiYBBYAWBgEAAoBoWIEUAQgSEGRwVHKYEBEi0UEtlYAlF3saYQhllgBQKP6KjARKEECwMhIWDmOAJAS4WAAAA.YAAAAAAAAAAA',gacm:'1~AAAAAAAAAAAiAABAAAgAIAAABAAhAAAACAAAAAAAQAQQAAAAAAABBBAAIAAAAAAAAAAAAQAAAIBAAAAAIgMAAAAAAAgAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAgAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAQAAAAAAFAAAABAAAAAAAAAAAARBAAAAAAAAAACAAABAAAAAAAAAAEAAAAAAABAAAAAEAAAAAAAAAAAAAAAAAAACBAAAAAAAAAAAAQAAAAAAAAAAgAAAAAAAQAAAAAAAAAAAAAAAACAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAgAAAAAAAEAAAAAAAQAAgAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAkQAAAAAAAAAAAAAAAAQ=',region:'fr'}; giosg_gid_4106=4wlrozdvpkaphfvqfqaafo32gokfhqar5sds4ascvqjaagam; giosg_chat_id_4106=aqj6iuzvgjde6q5jlmaaoz6pf24bwzugofytlyzw6bt4asim; giosg_gsessid_4106=bb7a679c-53c0-11ec-872e-0242ac120018; _yit.search=1; YIT-SearchLeads-19190={}; _yit.visited=1; YIT-lvi=['a:cityv62u-q27j-49ue-j59q86mus34t']; YIT-SearchTabs-19190={'main':['apartments','partments-list'],'products':['apartments','apartments-list']}"
    }


    url = 'https://www.yit.sk/api/v1/productsearch/apartments'
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.status_code)

    data = r.json()
    total_pages = data['TotalHits']

    payload['PageSize'] = total_pages

    url = 'https://www.yit.sk/api/v1/productsearch/apartments'
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.status_code)

    data = r.json()['Hits']

    apartment_data = []
    project_data = []

    scrapingDate = datetime.today().strftime('%Y-%m-%d')

    for item in data:

        apartment_dict = {

            "ApartmentName": None,
            "ApartmentAddress": None,
            "NumberOfRooms": None,
            "AppartmentFloor" : None,
            "ApartmentSize": None,
            "TotalAreaSize": None,
            "BalconySize" : None,
            "ReservationStatus": None,
            "SalesPrice": None,
            "ScrapingDate": scrapingDate,
            "ProjectName": None,
            "ProjectID": None,
        }

        project_dict = {
            "ProjectName": None,
            "ProjectAddress":None,
            "ProjectTotalApartments": None,
            "ProjectAvailableApartments": None,
            "ScrapingDate": scrapingDate
        }  

        #Fill Apartment dict values
        try:
            apartment_dict['ApartmentName'] = item['Fields']['ApartmentNumber']
        except KeyError:
            pass

        try:
            apartment_dict['ApartmentAddress'] = item['Fields']['ApartmentAddress']
        except KeyError:
            pass

        try:
            apartment_dict['NumberOfRooms'] = item['Fields']['NumberOfRooms']
        except KeyError:
            pass

        try:
            apartment_dict['AppartmentFloor'] = item['Fields']['FloorNumber']
        except KeyError:
            pass

        try:
            apartment_dict['ApartmentSize'] = item['Fields']['ApartmentSize']
        except KeyError:
            pass

        try:
            apartment_dict['TotalAreaSize'] = item['Fields']['TotalAreaSize']
        except KeyError:
            pass

        try:
            apartment_dict['BalconySize'] = item['Fields']['BalconySize']
        except KeyError:
            pass

        try:
            apartment_dict['ReservationStatus'] = item['Fields']['ReservationStatus']
        except KeyError:
            pass

        try:
            apartment_dict['SalesPrice'] = item['Fields']['SalesPrice']
        except KeyError:
            pass

        try:
            apartment_dict['ProjectName'] = item['Fields']['ProjectMarketingName']
        except KeyError:
            pass

        # Fill Project dict values

        if not any(project['ProjectName'] == item['Fields']['ProjectMarketingName'] for project in project_data):
            try:
                project_dict['ProjectName'] = item['Fields']['ProjectMarketingName']
            except KeyError:
                pass
            
            try:
                project_dict['ProjectAddress'] = item['Fields']['Address']
            except KeyError:
                pass
            
            try:
                project_dict['ProjectTotalApartments'] = item['Fields']['ProjectNumberOfApartments']
            except KeyError:
                pass
            
            try:
                project_dict['ProjectAvailableApartments'] = 1
            except KeyError:
                pass

            project_data.append(project_dict)
        else:
            for index, project in enumerate(project_data):
                if project['ProjectName'] == item['Fields']['ProjectMarketingName']:
                    project_data[index]['ProjectAvailableApartments'] = project_data[index]['ProjectAvailableApartments']+1
                    break

                
        apartment_data.append(apartment_dict)    

    postApartmentUrl = 'http://127.0.0.1:8000/apartments'
    statusUrl = 'http://127.0.0.1:8000/status'
    postProjectUrl = 'http://127.0.0.1:8000/projects'
    availabilityUrl = 'http://127.0.0.1:8000/availability'

    for project in project_data:
        db_project = findProjectInDB(project) 
        if db_project != None: #if the project is already in the db
            db_projectAvailability = findTodaysAvailability(db_project)
            if db_projectAvailability != None: #if there is a availability for today in db - update its values
                updated_availability={
                    'Project': db_project['ProjectID'],
                    'ProjectAvailableApartments': project['ProjectAvailableApartments'],
                    'ScrapingDate': project['ScrapingDate']           
                }
                response = requests.put(availabilityUrl, json = updated_availability)
                if(response.status_code == 200):
                    print(f"Successfully updated availability for project: {db_project['ProjectName']}")
                else:
                    print(f"Failed to update availability for project: {project['ProjectName']}")
            else: #if there is no availability in the db for today
                availability={
                    'Project': db_project['ProjectID'],
                    'ProjectAvailableApartments': project['ProjectAvailableApartments'],
                    'ScrapingDate': project['ScrapingDate']        
                }
                response = requests.post(availabilityUrl, json = availability)
                if(response.status_code == 200):
                    print(f"Successfully input todays availability for project: {db_project['ProjectName']}")
                else:
                    print(f"Failed to input todays availability for project: {project['ProjectName']}")
        else: #if the project is not yet in the db
            projectData = {
                "ProjectName": project['ProjectName'],
                "ProjectAddress": project['ProjectAddress'],
                "ProjectTotalApartments": project['ProjectTotalApartments'],
                "ScrapingDate": project['ScrapingDate']
            }
            response = requests.post(postProjectUrl, json = projectData)
            if(response.status_code == 200):
                last_project = getLastProjectInDB()
                availability={
                    'Project': last_project['ProjectID'],
                    'ProjectAvailableApartments': project['ProjectAvailableApartments'],
                    'ScrapingDate': project['ScrapingDate']
                }
                response = requests.post(availabilityUrl, json = availability)
                if(response.status_code == 200):
                    print(f"Successfully input project: {project['ProjectName']}, and accompanying availability")
                else:
                    print(f"Successfully input project: {project['ProjectName']}, but NOT the availability")
            else:
                print(f"Failed to imput project: {project['ProjectName']}")

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