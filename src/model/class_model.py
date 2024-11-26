class Field:
    def __init__(self, name):
        self.name = name
    
    # Using eq and hash allows us to more easily compare fields and check for list membership
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

# Since no types are required, parameters are just stored as a list of strings
#   self.name => str
#   self.params => List[str]
class Method:
    # params has the empty list as a default value, so that we can check for list membership easily
    def __init__(self, name: str, params: list[str] = []):
        self.name = name
        self.params = params

    # Using eq and hash allows us to more easily compare fields and check for list membership
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

class Class:
    # Creates a new class object with paremeters name and an empty set list for attributes#
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.methods = []
        #hidden x and y for 
        self.position = None
