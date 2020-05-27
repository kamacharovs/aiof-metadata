# Finance class that ties it all together

class Finance():
    def __init__(self, assets, liabilities, goals):
        self.assets = assets
        self.liabilities = liabilities
        self.goals = goals


    def get_total_assets_value(self):
        total = 0
        for a in self.assets:
            total += a.value
        return total

    def get_distinct_assets_types(self):
        assets_types = []
        for at in self.assets:
            if at.type not in assets_types:
                assets_types.append(at.type)
        return assets_types

    def get_total_liabilities_value(self):
        total = 0
        for l in self.liabilities:
            total += l.value
        return total

