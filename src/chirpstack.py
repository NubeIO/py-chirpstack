import requests


class Chirpstack:
    def __init__(self,
                 chirpstack_url=None,
                 chirpstack_user=None,
                 chirpstack_pass=None,
                 jwt=None
                 ):
        self.chirpstack_url = chirpstack_url
        self.chirpstack_user = chirpstack_user
        self.chirpstack_pass = chirpstack_pass
        self.jwt = jwt
        self.connect()

    def _authenticate(self):
        auth_url = "%s/api/internal/login" % self.chirpstack_url
        payload = {
            "email": self.chirpstack_user,
            "password": self.chirpstack_pass
        }
        auth_request = requests.post(
            auth_url,
            json=payload
        )
        auth_tok = auth_request.json()
        self.jwt = auth_tok.get('jwt')
        auth_header = {"Grpc-Metadata-Authorization": self.jwt}
        return auth_header

    def connect(self):
        auth_header = self._authenticate()
        is_connect = requests.Session()
        is_connect.headers = auth_header
        self.connection = is_connect

    def get_jwt(self):
        return self.jwt
