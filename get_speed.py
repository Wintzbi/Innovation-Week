from zwift import Client

username = "leynaickd@gmail.com"
password = "@Ymdthw62"
player_id = 7160265
client = Client(username, password)

world = client.get_world()
print(f"World ID: {world.world_id}")

profile = client.get_profile()
print(f"Player ID: {profile.player_id}")

player_status = world.player_status(player_id)

print(f"Vitesse actuelle du joueur : {player_status.player_state["speed"]}")


