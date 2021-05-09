# Interacting with the Chirpstack API to manage devices
import uuid
import binascii
import json

from src.utils.utils import Utils


class Devices:
    def __init__(self,
                 name=None,
                 description=None,
                 appid=None,
                 profile_id=None,
                 referenceAltitude=0,
                 skipFCntCheck=False,
                 deveui=None,
                 appKey=None,
                 nwkkey=None,
                 chirpstack_connection=None
                 ):
        self.name = name
        self.description = description
        self.appid = appid
        self.profile_id = profile_id
        self.referenceAltitude = referenceAltitude
        self.skipFCntCheck = skipFCntCheck
        self.deveui = deveui
        self.appKey = '00000000000000000000000000000000'
        self.nwkKey = nwkkey
        self.cscx = chirpstack_connection
        self.validate()

    def validate(self):
        deveui_target_len = 16
        nwkkey_target_len = 32
        appkey_target_value = '00000000000000000000000000000000'
        if self.deveui is not None and len(self.deveui) != deveui_target_len:
            raise ValueError(
                'DevEUI is %s characters in length, it should be 16' %
                len(self.deveui)
            )
        if self.nwkKey is not None and len(self.nwkKey) != nwkkey_target_len:
            raise ValueError(
                'NwkKey is %s characters in length, it should be 16' %
                len(self.nwkKey)
            )
        if self.appKey is not None and self.appKey != appkey_target_value:
            raise ValueError(
                'NwkKey %s does not match %s' %
                (
                    self.appKey,
                    appkey_target_value
                )
            )
        return True

    def create_and_activate(self):
        return_dict = {'result': 'success'}
        # Verify that we have all the information that we need
        if self.deveui is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "DevEUI was not provided"

        if self.appid is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Application ID was not provided"

        if self.profile_id is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Profile ID was not provided"

        if self.name is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device Name was not provided"

        if self.description is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device description was not provided"

        if return_dict['result'] == 'failure':
            return return_dict

        # Setup the payload
        device = {'application_id': self.appid, 'device_profile_id': self.profile_id,
                  'referenceAltitude': self.referenceAltitude, 'skipFCntCheck': self.skipFCntCheck, 'name': self.name,
                  'description': self.description, 'devEUI': self.deveui}

        payload = {'device': device}
        create_device = self.cscx.connection.post(
            self.cscx.chirpstack_url + "/api/devices",
            json=payload
        )

        if create_device.status_code == 200:
            if self.nwkKey is None:
                self.nwkKey = uuid.uuid4().hex
            keys_payload = {
                "deviceKeys": {
                    "nwkKey": self.nwkKey,
                    "devEUI": self.deveui,
                    "appKey": self.appKey
                }
            }

            set_keys = self.cscx.connection.post(
                self.cscx.chirpstack_url + "/api/devices/" + self.deveui + "/keys",
                json=keys_payload
            )

            if set_keys.status_code == 200:
                printable_dev_eui = ', '.join(
                    hex(i) for i in binascii.unhexlify(self.deveui)
                )
                printable_nwk_key = ', '.join(
                    hex(i) for i in binascii.unhexlify(self.nwkKey)
                )
                return_dict['result'] = "success"
                return_dict['printable_dev_eui'] = printable_dev_eui
                return_dict['printable_nwk_key'] = printable_nwk_key
            else:
                return_dict['result'] = ['failure']
                return_dict['message'] = "Error: %s" % json.loads(
                    set_keys.content
                )['message']
                self.cscx.connection.delete(
                    self.cscx.chirpstack_url + "/api/devices/" + self.deveui,
                )
        else:
            return_dict['result'] = "failure"
            return_dict['message'] = json.loads(
                create_device.content
            )['message']
        return return_dict

    def update(self, dev_eui):
        return_dict = {'result': 'success'}
        # Verify that we have all the information that we need
        if self.deveui is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "DevEUI was not provided"

        if self.appid is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Application ID was not provided"

        if self.profile_id is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Profile ID was not provided"

        if self.name is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device Name was not provided"

        if self.description is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "Device description was not provided"

        if return_dict['result'] == 'failure':
            return return_dict

        # Setup the payload
        device = {'application_id': self.appid, 'device_profile_id': self.profile_id,
                  'referenceAltitude': self.referenceAltitude, 'skipFCntCheck': self.skipFCntCheck, 'name': self.name,
                  'description': self.description, 'devEUI': self.deveui}

        payload = {'device': device}
        url = f"{self.cscx.chirpstack_url}/api/devices/{dev_eui}"
        res = self.cscx.connection.put(url, json=payload)
        return Utils.http_response(res)

    def delete(self, dev_eui):
        return_dict = {'result': 'success'}
        if dev_eui is None:
            return_dict['result'] = 'failure'
            return_dict['message'] = "DevEUI was not provided"
        if return_dict['result'] == 'failure':
            return return_dict
        url = f"{self.cscx.chirpstack_url}/api/devices/{dev_eui}"
        res = self.cscx.connection.get(url)
        return Utils.http_response(res)

    def list_all(self,
                 appid: int = 1,
                 limit: int = 100
                 ):
        """
        list all gateways
        :param appid:
        :param limit:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/devices?limit={limit}&applicationID={appid}"
        res = self.cscx.connection.get(url)
        return Utils.http_response_json(res)

    def get_device(self,
                   dev_eui: str = None,
                   ):
        """
        get gateway stats
        :param dev_eui:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/devices/{dev_eui}"
        res = self.cscx.connection.get(url)
        return Utils.http_response_json(res)
