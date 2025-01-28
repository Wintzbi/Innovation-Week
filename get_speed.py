from zwift import Client
import time

username = "leynaickd@gmail.com"
password = "@Ymdthw62"
player_id = 7160265
client = Client(username, password)

world = client.get_world()
print(f"World ID: {world.world_id}")

profile = client.get_profile()
print(f"Player ID: {profile.player_id}")

while world.world_id == 1:
    player_status = world.player_status(player_id)
    print("Vitesse actuelle du joueur :", player_status.player_state.__getattribute__("speed")*0.00001)
    time.sleep(1)



