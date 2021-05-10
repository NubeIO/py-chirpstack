from chirpstack.utils.utils import Utils


class Gateway:
    def __init__(self,
                 organizationID=None,
                 chirpstack_connection=None
                 ):
        self.organizationID = organizationID
        self.cscx = chirpstack_connection

    def list_all(self,
                 organizationID: int = 1,
                 limit: int = 100
                 ):
        """
        list all gateways
        :param organizationID:
        :param limit:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/gateways?limit={limit}&organizationID={organizationID}"
        res = self.cscx.connection.get(url)
        return Utils.http_response_json(res)

    def get_gateway(self,
                    gateway_id: str = None,
                    ):
        """
        get gateway stats
        :param gateway_id:
        :return:
        """
        url = f"{self.cscx.chirpstack_url}/api/gateways/{gateway_id}"
        res = self.cscx.connection.get(url)
        return Utils.http_response_json(res)

    def stats(self,
              gateway_id: str = None,
              days: int = None
              ):
        """
        get gateway stats
        :param gateway_id:
        :param days:
        :return:
        """
        sub_days = Utils.encode_time(Utils.day_subtract(days))
        now = Utils.encode_time(Utils.time_now())
        interval = "DAY"
        url = f"{self.cscx.chirpstack_url}/api/gateways/{gateway_id}/stats?interval={interval}&startTimestamp={sub_days}&endTimestamp={now}"
        res = self.cscx.connection.get(url)
        return Utils.http_response_json(res)
