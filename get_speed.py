import sys
import time
import serial
from zwift import Client
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)

MAX_BUFF_LEN = 255
SETUP 		 = False
port 		 = None

prev = time.time()
while(not SETUP):
	try:
		port = serial.Serial("COM4", 115200, timeout=1)
	except: # Bad way of writing excepts (always know your errors)
		if(time.time() - prev > 2): # Don't spam with msg
			print("No serial detected, please plug your uController")
			prev = time.time()
            

	if(port is not None): # We're connected
		SETUP = True
		print("Connected...")
          
# read one char (default)
def read_ser(num_char = 1):
    string = port.read(num_char)
    return string.decode()

# Write whole strings
def write_ser(cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())
     
class ZwiftApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zwift Application")

        self.email_label = QLabel("Adresse e-mail :")
        self.email_input = QLineEdit()

        self.password_label = QLabel("Mot de passe :")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.player_id_label = QLabel("ID du joueur :")
        self.player_id_input = QLineEdit()

        self.start_button = QPushButton("Lancer l'application")
        self.start_button.clicked.connect(self.start_application)

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.player_id_label)
        layout.addWidget(self.player_id_input)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_application(self):
        email = self.email_input.text()
        password = self.password_input.text()
        player_id = self.player_id_input.text()

        if not email or not password or not player_id:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            player_id = int(player_id)
            client = Client(email, password)
            world = client.get_world()

            QMessageBox.information(
                self, "Connexion réussie", f"Connexion réussie au monde ID : {world.world_id}"
            )

            self.track_player_speed(client, world, player_id)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def track_player_speed(self, client, world, player_id):
        try:
            while world.world_id == 1:
                player_status = world.player_status(player_id)
                speed = player_status.player_state.__getattribute__("speed") * 0.000001
                power = player_status.player_state.__getattribute__("power")
                calories = player_status.player_state.__getattribute__("calories") * 0.001
                heartrate = player_status.player_state.__getattribute__("heartrate")
                distance = player_status.player_state.__getattribute__("distance") * 0.001
                cadence = player_status.player_state.__getattribute__("cadenceUHz") * 0.0001
                write_ser(str(speed)+','+str(power)+','+str(calories)+','+str(heartrate)+','+str(distance)+','+str(cadence))
                string = read_ser(MAX_BUFF_LEN)
                if(len(string)):
                    print(string)
                time.sleep(0.4)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur dans le suivi de la vi@tesse : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZwiftApp()
    window.show()
    sys.exit(app.exec_())





