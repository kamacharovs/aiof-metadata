# Financial Goals
#   - Mandatory short-term goals

class Goal:
    _types = [
        "short-term",
        "long-term"
    ]

    def __init__(self, name, type):
        self.name = name
        self.type = type if type in self._types else "other"
        self.savings = False