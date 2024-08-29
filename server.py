import socket
from mud.networking.connection import Connection
from mud.game.gameloop import GameLoop

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.connections = {}

    def accept_new_connection(self):
        """
        Accept new incoming connections and create Connection objects.
        """
        try:
            client_sock, client_addr = self.server_socket.accept()
            connection = Connection(client_sock, client_addr)
            self.connections[client_sock] = connection
            print(f"New connection from {client_addr}")
            connection.begin_character_creation()  # Start character creation for new connection
        except socket.error:
            pass

    def process_player_input(self, connection, data):
        """
        Process player input. Directs to character creation if the character is new.
        """
        if connection.character.is_new:
            connection.process_creation_input(data)
        else:
            # Regular gameplay input handling goes here
            if data.lower() == "quit":
                connection.send_message("Goodbye!")
                self.remove_connection(connection)
            else:
                connection.send_message(f"You said: {data}")

    def remove_connection(self, connection):
        """
        Remove a player's connection and close the socket.
        """
        print(f"Connection closed: {connection.address}")
        connection.close()
        del self.connections[connection.sock]

    def close(self):
        """
        Close all connections and the server socket.
        """
        for connection in self.connections.values():
            connection.close()
        self.server_socket.close()
        print("Server shut down.")


if __name__ == "__main__":
    server = Server("localhost", 4000)
    game_loop = GameLoop(server, tick_rate=1.0)  # Set the tick rate to 1 second

    try:
        game_loop.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        game_loop.stop()
        server.close()