from src import device, chirpstack, device_profiles, gateway


# Setup the connection
cx = chirpstack.Chirpstack(
    chirpstack_url="http://123.209.90.112:8080",
    chirpstack_user="admin",
    chirpstack_pass="admin"
)

# Connect to the device class
g = gateway.Gateway(chirpstack_connection=cx)

# Get all the devices
gateways = g.list_all(organizationID=1)
print(gateways)
print("We found %s gateways" % gateways['totalCount'])
# for res in gateways['result']:
#     for key, val in res.items():
#         print("%s => %s" % (key, val))
#     print("==========")

stat = g.stats(gateway_id='0000000000000000', days=10)

print(stat)