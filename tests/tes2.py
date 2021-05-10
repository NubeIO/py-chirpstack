from chirpstack import device, chirpstack, device_profiles

# Setup the connection
cx = chirpstack.Chirpstack(
    chirpstack_url="http://123.209.90.112:8080",
    chirpstack_user="admin",
    chirpstack_pass="admin"
)

# Connect to the device class
d = device.Devices(chirpstack_connection=cx)

dp = device_profiles.DeviceProfiles(
    chirpstack_connection=cx)

# Get all the devices
devices = d.list_all(2)
dplist = dp.list()
print(dplist)
# print("We found %s devices" % devices['totalCount'])
# for dev in devices['result']:
#     for key, val in dev.items():
#         print("%s => %s" % (key, val))
#     print("==========")


# d = device.Devices(chirpstack_connection=cx)
d.description = "This is my device"
d.deveui = "c9014a013d89fa5c"
d.name = "My-device-name22111122"
d.profile_id = "08b4a5e4-552f-4a1e-aba6-dbda739a152e"
d.appid = 1
# d.nwkKey = "MyRandomHexStrings"
res = d.delete()
# res = d.create_and_activate()
print(res)

# res = d.update()
print(res)
