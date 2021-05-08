from src.utils.utils import Utils


class Gateway:

    def __init__(self,
                 organizationID=None,
                 chirpstack_connection=None
                 ):
        self.organizationID = organizationID
        self.cscx = chirpstack_connection

    def list_all(self,
                 organizationID=None,
                 limit=100
                 ):
        """
        list all gateways
        :param organizationID:
        :param limit:
        :return:
        """
        gateways_list_query = "%s/api/gateways?limit=%s&organizationID=%s" % (
            self.cscx.chirpstack_url,
            limit,
            organizationID
        )
        r = self.cscx.connection.get(gateways_list_query).json()
        return r

    def stats(self,
              gateway_id=None,
              days=None
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
        print(sub_days, now)
        url = f"{self.cscx.chirpstack_url}/api/gateways/{gateway_id}/stats?interval={interval}&startTimestamp={sub_days}&endTimestamp={now}"
        r = self.cscx.connection.get(url).json()
        return r
