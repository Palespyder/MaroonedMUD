class Stat:
    def __init__(self, name, current=0, max_value=100, min_value=0):
        self.name = name
        self.current = current
        self.max_value = max_value
        self.min_value = min_value
        self.modifiers = []

    def add_modifier(self, modifier):
        """Add a modifier to the stat."""
        self.modifiers.append(modifier)

    def calculate_effective_value(self):
        """Calculate the stat value including modifiers."""
        effective_value = self.current
        for modifier in self.modifiers:
            effective_value += modifier
        return min(max(self.min_value, effective_value), self.max_value)
    
    def __repr__(self):
        return (f"Stat(name={self.name}, current={self.current}, "
                f"max_value={self.max_value}, min_value={self.min_value}, "
                f"modifiers={self.modifiers})")
    


class Stats:
    def __init__(self):
        self.stats = {}

    def add_stat(self, name, current=0, max_value=100, min_value=0):
        """Create a new stat and add it to the stats dictionary."""
        if name in self.stats:
            raise ValueError(f"Stat '{name}' already exists.")
        self.stats[name] = Stat(name, current, max_value, min_value)

    def get_stat(self, name):
        """Retrieve a stat by its name."""
        return self.stats.get(name, None)

    def modify_stat(self, name, amount):
        """Modify the current value of a stat."""
        stat = self.get_stat(name)
        if stat:
            stat.current = min(max(stat.min_value, stat.current + amount), stat.max_value)
        else:
            raise ValueError(f"Stat '{name}' does not exist.")

    def apply_modifier(self, name, modifier):
        """Apply a modifier to a specific stat."""
        stat = self.get_stat(name)
        if stat:
            stat.add_modifier(modifier)
        else:
            raise ValueError(f"Stat '{name}' does not exist.")
        
    def list_stats(self):
        """Returns a list of stats and their details."""
        return [
            {
                "name": stat.name,
                "current": stat.current,
                "max_value": stat.max_value,
                "min_value": stat.min_value,
                "modifiers": stat.modifiers,
            }
            for stat in self.stats.values()
        ]

    def __repr__(self):
        return f"Stats({self.stats})"