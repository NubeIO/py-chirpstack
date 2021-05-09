import json


class Users:
    def __init__(self,
                 chirpstack_connection=None
                 ):
        self.cscx = chirpstack_connection

    def list_all(self,
                 limit: int = 100
                 ):
        """
        list all users
        :param limit:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/users?limit={limit}"
        return self.cscx.connection.get(url).json()

    def get_user(self,
                 _id: int = 1
                 ):
        """
        get gateway stats
        :param _id:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/users/{_id}"
        return self.cscx.connection.get(url).json()

    def update_user_password(self,
                             _id: int = None,
                             password: str = None
                             ):
        """
        get gateway stats
        :param _id:
        :param password:
        :return:
        """
        return_dict = {'result': 'success'}
        if password is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "password was not provided"

        if return_dict['result'] == 'failure':
            return return_dict
        payload = {'password': password, 'userId': _id}
        url = f"{self.cscx.chirpstack_url}/api/users/{_id}/password"
        user = self.cscx.connection.put(url, json=payload)
        if user.status_code != 200:
            return_dict['result'] = "failure"
            return_dict['message'] = json.loads(
                user.content
            )['message']

        return return_dict
