# Finance class that ties it all together

class Finance():
    def __init__(self, assets, liabilities, goals):
        self.assets = assets
        self.liabilities = liabilities
        self.goals = goals


    def get_total_assets_value(self):
        return sum(self.assets.value)
    def get_distinct_assets_types(self):
        return list(set(assets.type))

    def get_total_liabilities_value(self):
        return sum(self.liabilities.value)

