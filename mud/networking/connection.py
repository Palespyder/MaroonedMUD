import socket
from mud.game.character import Character

class Connection:
    def __init__(self, sock, address):
        self.sock = sock
        self.address = address
        self.character = Character()  # Initialize a new character for this connection
        self.creation_step = 0  # Track which step of character creation the player is on

    def receive_data(self):
        """
        Receive data from the client.
        """
        try:
            data = self.sock.recv(1024).decode('utf-8').strip()
            if data:
                return data
        except socket.error:
            pass
        return None

    def send_message(self, message):
        """
        Send a message to the client.
        """
        try:
            self.sock.sendall((message + "\n").encode('utf-8'))
        except socket.error:
            print(f"Failed to send message to {self.address}")

    def close(self):
        """
        Close the connection.
        """
        try:
            self.sock.close()
        except socket.error:
            pass

    def begin_character_creation(self):
        """
        Start the character creation process.
        """
        self.creation_step = 1
        self.send_message("Welcome to the MUD! Let's create your character.")
        self.send_message("Please enter your character's name:")

    def process_creation_input(self, data):
        """
        Process input during the character creation process.
        """
        if self.creation_step == 1:
            self.character.set_name(data)
            self.creation_step += 1
            self.send_message(f"Great, {self.character.name}! Now choose your class: Warrior, Mage, or Rogue.")
        elif self.creation_step == 2:
            self.character.set_class(data.capitalize())
            self.creation_step += 1
            self.character.is_new = False  # Character creation is complete
            self.send_message("Character creation complete! Here is your character sheet:")
            self.send_message(self.character.display_character_sheet())
            self.send_message("You are now entering the game...")
            # Here you would place the character in the game world, etc.
        else:
            self.send_message("Invalid input during character creation.")


