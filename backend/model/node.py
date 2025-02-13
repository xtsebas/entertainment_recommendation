from datetime import date
from typing import List, Optional

class Node:
    def __init__(self, node_id: str, label: str, **properties):
        self.node_id = node_id
        self.label = label
        self.properties = properties

    def to_dict(self):
        return {
            'id': self.node_id,
            'label': self.label,
            'properties': self.properties
        }