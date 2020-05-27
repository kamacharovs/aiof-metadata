# Anything that you are paying interest on:
#   - Credit card
#   - Student loans
#   - Car loan
#   - Mortgage
#   - House renovation
#   - RV
#   - Any personal loan
#   - Etc.

class Liability:
    _types = [
        "credit card",
        "car loan",
        "mortgage",
        "house renovation",
        "rv",
        "personal loan",
        "loan",
        "other"
    ]

    def __init__(self, name, type, value):
        self.name = name
        self.type = type if type in self._types else "other"
        self.value = value