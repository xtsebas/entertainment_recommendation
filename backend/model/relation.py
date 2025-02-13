from model.node import Node

class Relation:
    def __init__(self, start_node: Node, relation_type: str, end_node: Node, **properties):
        self.start_node = start_node
        self.relation_type = relation_type
        self.end_node = end_node
        self.properties = properties

    def to_dict(self):
        return {
            'start': self.start_node.to_dict(),
            'relation': self.relation_type,
            'end': self.end_node.to_dict(),
            'properties': self.properties
        }