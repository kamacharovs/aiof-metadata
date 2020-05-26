class Asset:
    _types = [
        "car",
        "house",
        "boat",
        "stock",
        "investment property",
        "cash",
        "other"
    ]

    def __init__(self, name, type, value):
        self.name = name
        self.type = type if type in _types else "other"
        self.value = value