import time
import select

class GameLoop:
    def __init__(self, server, tick_rate=1.0):
        """
        Initialize the game loop.
        :param server: The game server instance handling connections.
        :param tick_rate: How often (in seconds) the game state should be updated.
        """
        self.server = server
        self.tick_rate = tick_rate
        self.running = False

    def start(self):
        """
        Start the game loop.
        """
        self.running = True
        print("Game loop started.")
        last_tick = time.time()

        while self.running:
            # Check for new connections
            self.server.accept_new_connection()

            # Check for incoming messages from players
            readable, _, _ = select.select(self.server.connections, [], [], 0.1)
            for sock in readable:
                connection = self.server.connections[sock]
                data = connection.receive_data()
                if data:
                    self.server.process_player_input(connection, data)

            # Update game state based on tick rate
            current_time = time.time()
            if current_time - last_tick >= self.tick_rate:
                self.update_game_state()
                last_tick = current_time

            # Small sleep to prevent busy-waiting
            time.sleep(0.01)

    def stop(self):
        """
        Stop the game loop.
        """
        self.running = False
        print("Game loop stopped.")

    def update_game_state(self):
        """
        Update the game state. This function gets called every tick.
        """
        # Example of what could be done each tick:
        # - NPC movements
        # - Environment changes (day/night cycle)
        # - Trigger timed events
        print("Game world updated.")

        # Broadcast a heartbeat to all connected players (optional)
        for connection in self.server.connections.values():
            connection.send_message("Tick: The world has been updated.")