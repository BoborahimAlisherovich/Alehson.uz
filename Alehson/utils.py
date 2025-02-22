import os
import requests
# from decouple import config

# Constants for status codes
SUCCESS = 200
PROCESSING = 102
FAILED = 400
INVALID_NUMBER = 160
MESSAGE_IS_EMPTY = 170
SMS_NOT_FOUND = 404
SMS_SERVICE_NOT_TURNED = 600

# Configuration (Using decouple for secure management)
ESKIZ_EMAIL = "boborahimrustamqulov0@gmail.com"
ESKIZ_PASSWORD = "boborahim007"

class SendSmsApiWithEskiz:
    def __init__(self, message, phone, email=ESKIZ_EMAIL, password=ESKIZ_PASSWORD):
        self.message = message
        self.phone = phone
        self.email = email
        self.password = password

    def send(self):
        """Main method to handle sending SMS after validation."""
        status_code = self.custom_validation()
        if status_code == SUCCESS:
            result = self.calculation_send_sms(self.message)
            if result == SUCCESS:
                return self.send_message(self.message)
            else:
                return result
        return status_code

    def custom_validation(self):
        """Validate phone number and message content."""
        if len(str(self.phone)) != 9:
            return INVALID_NUMBER
        if not self.message:
            return MESSAGE_IS_EMPTY
        else:
            self.message = self.clean_message(self.message)
        return SUCCESS

    def authorization(self):
        """Get authorization token from Eskiz API."""
        data = {
            'email': self.email,
            'password': self.password,
        }

        AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'
        try:
            r = requests.post(AUTHORIZATION_URL, data=data)
            r.raise_for_status()  # Check if the request was successful
            response_data = r.json()
            token = response_data.get('data', {}).get('token')
            if token:
                return token
            else:
                raise ValueError("Token missing in response.")
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except ValueError as ve:
            return {"error": str(ve)}

    def send_message(self, message):
        """Send SMS via Eskiz API."""
        token = self.authorization()
        if 'error' in token:
            return token  # If authorization failed, return the error
        
        SEND_SMS_URL = "http://notify.eskiz.uz/api/message/sms/send"
        PAYLOAD = {
            'mobile_phone': '998' + str(self.phone),
            'message': message,
            'from': '4546',
            'callback_url': 'http://afbaf9e5a0a6.ngrok.io/sms-api-result/'
        }

        HEADERS = {
            'Authorization': f'Bearer {token}'
        }

        try:
            r = requests.post(SEND_SMS_URL, headers=HEADERS, data=PAYLOAD)
            r.raise_for_status()  # Check if request was successful
            return r.json()  # Return the response JSON from Eskiz
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to send SMS: {str(e)}"}

    def get_status(self, id):
        """Check the status of a sent SMS."""
        token = self.authorization()
        if 'error' in token:
            return token  # If authorization failed, return the error
        
        CHECK_STATUS_URL = f'http://notify.eskiz.uz/api/message/sms/status/{id}'
        HEADERS = {
            'Authorization': f'Bearer {token}'
        }

        try:
            r = requests.get(CHECK_STATUS_URL, headers=HEADERS)
            r.raise_for_status()
            response_data = r.json()
            if response_data['status'] == 'success':
                status = response_data['message']['status']
                if status == 'DELIVRD' or status == 'TRANSMTD':
                    return SUCCESS
                elif status == 'EXPIRED':
                    return FAILED
                else:
                    return PROCESSING
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to check SMS status: {str(e)}"}

    def clean_message(self, message):
        """Clean and replace certain characters in the message."""
        substitutions = {
            'ц': 'ts', 'ч': 'ch', 'ю': 'yu', 'а': 'a', 'б': 'b', 'қ': 'q', 'ў': "o'", 
            'ғ': "g'", 'ҳ': "h", 'х': "x", 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 
            'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 
            'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 
            'у': 'u', 'ш': 'sh', 'щ': 'sh', 'ф': 'f', 'э': 'e', 'ы': 'i', 'я': 'ya', 
            'ў': "o'", 'ь': "'", 'ъ': "'", '’': "'", '“': '"', '”': '"', ',': ',', 
            '.': '.', ':': ':', 'Ц': 'Ts', 'Ч': 'Ch', 'Ю': 'Yu', 'А': 'A', 'Б': 'B', 
            'Қ': "Q", 'Ғ': "G'", 'Ҳ': "H", 'Х': "X", 'В': 'V', 'Г': 'G', 'Д': 'D', 
            'Е': 'E', 'Ё': 'Yo', 'Ж': 'J', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 
            'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 
            'Т': 'T', 'У': 'U', 'Ш': 'Sh', 'Щ': 'Sh', 'Ф': 'F', 'Э': 'E', 'Я': 'Ya'
        }

        for old, new in substitutions.items():
            message = message.replace(old, new)
        
        return message

    def calculation_send_sms(self, message):
        """Calculate number of SMS required based on message length."""
        try:
            length = len(message)
            if length <= 160:
                self.spend = 1
            elif length <= 306:
                self.spend = 2
            elif length <= 459:
                self.spend = 3
            elif length <= 612:
                self.spend = 4
            elif length <= 765:
                self.spend = 5
            elif length <= 918:
                self.spend = 6
            elif length <= 1071:
                self.spend = 7
            elif length <= 1224:
                self.spend = 8
            else:
                self.spend = 30

            return SUCCESS
        except Exception as e:
            return FAILED
