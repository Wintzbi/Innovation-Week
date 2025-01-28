import sys
import time
from zwift import Client
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)


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
                speed = player_status.player_state.__getattribute__("speed") * 0.00001
                print("Vitesse actuelle du joueur :", speed)
                time.sleep(1)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur dans le suivi de la vitesse : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZwiftApp()
    window.show()
    sys.exit(app.exec_())
