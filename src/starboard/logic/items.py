class Item:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def item_action(self):
        print(f"Item {self.name} activated")

    def print_item_data(self):
        print(f"Name: {self.name}:\n"
              f"Description:\n{self.desc}")