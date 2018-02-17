import requests
from stellar import settings
from utils import ValidationException


class KaKaoTalk:
    @staticmethod
    def account_verification(access_token):
        # API Response = UID, Expires Time, appID
        url = 'https://kapi.kakao.com/v1/user/access_token_info'
        header = {'Authorization': 'Bearer ' + access_token}
        # status code 400 = Validation Error, 401 code = Token Expiration
        # response has uid, expiresInMillis, appId
        response = requests.get(url, headers=header)
        response_dict = response.json()

        if response.status_code == 400:
            raise ValidationException('Account Verification Validation Error')
        elif response.status_code == 401:
            raise ValidationException('Token Expiration')

        return response_dict

    # @staticmethod
    # def get_account_info(access_token):
    #     url = 'https://kapi.kakao.com/v1/user/me'
    #     header = {'Authorization': 'Bearer ' + access_token}
    #     response = requests.get(url, headers=header)
    #     response_dict = response.json()
    # 
    #     return response_dict


class FaceBook:
    # Response = data{UID, ETC...}
    @staticmethod
    def account_verification(access_token):
        url = 'https://graph.facebook.com/debug_token'
        param = {
            'input_token': access_token,
            'access_token': settings.CONF_FILE['FACEBOOK']['APP_ACCESS_TOKEN']
        }
        response = requests.get(url, params=param)
        response_dict = response.json()
        is_valid = response_dict['data']['is_valid']

        if not is_valid:
            raise ValidationException('Invalid Access Token')
        
        return response_dict

    # @staticmethod
    # def get_account_info(access_token):
    #     url = 'https://graph.facebook.com/me?fields=id,name,email'
    #     header = {'Authorization': 'Bearer ' + access_token}
    #     param = {
    #         'fields': 'id,name,email'
    #     }
    # 
    #     response = requests.get(url, params=param, headers=header)
    #     response_dict = response.json()
    #     return response_dict
