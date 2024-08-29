class Character:
    def __init__(self, name=None, character_class=None):
        """
        Initialize a new character.
        :param name: The character's name.
        :param character_class: The character's class (if applicable).
        """
        self.name = name
        self.character_class = character_class
        self.attributes = {'strength': 10, 'dexterity': 10, 'intelligence': 10}  # Default attributes
        self.inventory = []  # List of items the character possesses
        self.location = None  # Starting location in the game world
        self.is_new = True  # Flag to indicate if the character is newly created

    def set_name(self, name):
        """
        Set the character's name.
        :param name: The desired name for the character.
        """
        self.name = name

    def set_class(self, character_class):
        """
        Set the character's class.
        :param character_class: The chosen class for the character.
        """
        self.character_class = character_class

    def display_character_sheet(self):
        """
        Display the character's attributes and other relevant information.
        """
        char_sheet = f"Name: {self.name}\n"
        char_sheet += f"Class: {self.character_class}\n"
        char_sheet += "Attributes:\n"
        for attr, value in self.attributes.items():
            char_sheet += f"  {attr.capitalize()}: {value}\n"
        return char_sheet