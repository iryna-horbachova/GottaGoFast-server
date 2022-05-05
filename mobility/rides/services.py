import requests


class AuthenticationManager:
    BASE_URL = 'http://localhost:8080/'
    USER_ID_ENDPOINT = 'api/profile/user/id'
    AUTHORIZATION_HEADER = 'Authorization'

    def get_user_id_or_none(self, headers):
        if self.AUTHORIZATION_HEADER not in headers:
            return None

        # Call authentication microservice
        url = self.BASE_URL + self.USER_ID_ENDPOINT
        user_id_request = requests.get(url, headers=headers)

        if user_id_request.status_code == 401:
            return None

        return user_id_request.json()['user_id']