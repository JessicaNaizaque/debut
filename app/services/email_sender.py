import requests
from dotenv import load_dotenv
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_directory, '..', '.env')
load_dotenv(dotenv_path)

class ApigClient:
    """
    Define the url and credentials to login db
    """
    def __init__(self):
        self.url = os.environ.get('APIG_URL')
        self.url_commonweb = os.environ.get('APIG_URL') + os.environ.get('APIG_URL_COMMONWEB')
        self.email = os.environ.get('APIG_USR')
        self.password = os.environ.get('APIG_PWD')
        self.email_to = os.environ.get('EMAIL_TO')
        
    """
    Login to get the token
    param: None
    return: token (str)
    """
    def login(self):
        url_login = self.url + "login"
        data = {"email": self.email, "password": self.password}

        response = requests.post(url_login, json=data, verify=False)

        if response.status_code == 200:
            response_data = response.json()
            token = response_data["data"][0]["result"]["token"]
            return token
        else:
            print(f"Request login apig failed with status code: {response.status_code}")
            print(response.text)
            return None

    def send_email(self, name, email, phone, school, subject, message):
        token = self.login()
        if token == None:
            return False
        
        if phone == None:
            phone = ""
        if school == None:
            school = ""
            
        url_email = self.url_commonweb + "notifications/v1/email"
        
        data = {
            "origin": "asesoriaseducativasaldia",
            "to": self.email_to,
            "subject": subject,
            "template": "i0_contact.0",
            "variables": ["aead", "Nombre:", name, "Email:", email, "Telefono:", phone, "Colegio:", school, "Mensaje:", message]
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Language": "es"
        }

        response = requests.post(url_email, json=data, headers=headers, verify=False)

        if response.status_code == 200:
            print(response.text)
            return True
        else:
            print(f"Request update user failed with status code {response.status_code}: {response.text}")
            return False