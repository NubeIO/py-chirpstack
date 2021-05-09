from src import chirpstack, gateway
from src.tests.test_settings import TestSettings

cx = chirpstack.Chirpstack(
    chirpstack_url=TestSettings.ip,
    chirpstack_user=TestSettings.user,
    chirpstack_pass=TestSettings.password
)

# Connect to the gateway class
g = gateway.Gateway(chirpstack_connection=cx)

# Get all the gateways
gateways = g.list_all(organizationID=1)
print(gateways)

# Get gateway
stat = g.get_gateway(gateway_id='0000000000000000')
print(stat)

# Get gateway stats
stat = g.stats(gateway_id='0000000000000000', days=10)
print(stat)
