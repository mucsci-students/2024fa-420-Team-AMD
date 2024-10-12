from enum import Enum

class Type(Enum):
    Aggregate = 1
    
    def display(self):
        match self:
            case Aggregate:
                return 'Aggregate'
    
    # Translates input into Relationship Type. Returns None on bad input
    def make(text):
        match text:
            case 'aggregate':
                return Type.Aggregate
            case _:
                return None
    
class Relationship:
    def __init__(self, src, dst, typ):
        self.src = src
        self.dst = dst
        self.typ = typ
    
    def __str__(self):
        return f'{{Src: {self.src}, Dst: {self.dst}, Typ: {self.typ.name}}}'
    
    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst

    def __hash__(self):
        return hash((self.src, self.dst, self.typ))
