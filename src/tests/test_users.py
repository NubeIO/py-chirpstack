from src import chirpstack, users
from src.tests.test_settings import TestSettings

cx = chirpstack.Chirpstack(
    chirpstack_url=TestSettings.ip,
    chirpstack_user=TestSettings.user,
    chirpstack_pass=TestSettings.password
)

# Connect to the device class
g = users.Users(chirpstack_connection=cx)

# Get all the users
u = g.list_all()
print(u)

# Get a user by id
u = g.get_user(1)
print(u)

# u = g.update_user_password(1, "N00BLWAN")
# print(u)
