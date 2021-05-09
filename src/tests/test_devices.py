from src import chirpstack, device
from src.tests.test_settings import TestSettings

cx = chirpstack.Chirpstack(
    chirpstack_url=TestSettings.ip,
    chirpstack_user=TestSettings.user,
    chirpstack_pass=TestSettings.password
)

# Connect to the gateway class
d = device.Devices(chirpstack_connection=cx)

# Get all the devices
devices = d.list_all(appid=1)
print(devices)

devices = d.get_device(dev_eui="a81758fffe056177")
print(devices)

# d = device.Devices(chirpstack_connection=cx)
d.description = "This is my device"
d.deveui = "c9014a013d89fa5c"
d.name = "My-device-32222"
d.profile_id = "08b4a5e4-552f-4a1e-aba6-dbda739a152e"
d.appid = 1
# d.nwkKey = "MyRandomHexStrings"
# res = d.delete()
# res = d.create_and_activate()
# print(res)

res = d.update()
print(res)