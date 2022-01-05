# importing annotations for type hinting in enclosing class
# see https://stackoverflow.com/q/33533148/13283436
from __future__ import annotations

from dataclasses import dataclass, field  # DataNode is a dataclass
from typing import List, Optional  # for type hinting


# Graph node that stores id, data (if any), and neighbours (if any)
@dataclass
class DataNode:
    """
    Class representation of Node that stores its id, int data, list of DataNode neighbours
    """
    identifier: int = field()
    data: Optional[int] = field(default=None)
    neighbours: List[DataNode] = field(default_factory=list)

    def neighbours_ids(self):
        return [neighbour.identifier for neighbour in self.neighbours]
