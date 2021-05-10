class DeviceProfiles:
    def __init__(self,
                 name=None,
                 description=None,
                 chirpstack_connection=None
                 ):
        self.cscx = chirpstack_connection

    def list(self,
             limit=10,
             offset=0,
             appid=None,
             orgid=None):
        """
        list all device-profiles
        :param limit:
        :param offset:
        :param appid:
        :param orgid:
        :return:
        """
        url = "%s/api/device-profiles?limit=%s&offset=%s" % (
                self.cscx.chirpstack_url,
                limit,
                offset)
        if appid is not None:
            url = "%s&applicationID=%s" % (url, appid)
        if orgid is not None:
            url = "%s&organizationID=%s" % (url, orgid)

        ret_list = self.cscx.connection.get(url)
        return ret_list.json()
