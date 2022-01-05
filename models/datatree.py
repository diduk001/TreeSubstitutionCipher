from collections import defaultdict  # used in BFS
from queue import SimpleQueue  # used in BFS
from random import getrandbits, choice, shuffle  # for building random trees
from typing import DefaultDict, Dict, List, Tuple, Optional, Callable, Any  # for type hinting

from datanode import DataNode  # Tree contains DataNodes

RANDOM_ID_BITS = 60


class DataTree:
    """
    Class representation of Tree which Nodes are :class:`models.datanode.DataNode`

    Initialization by default is empty block_tree
    """

    nodes: List[DataNode]

    def __init__(self):
        self.nodes = list()

    def get_node_by_id(self, identifier: int) -> DataNode:
        """
        Returns Node by Identifier
        If Node with such Identifier is not present, raises KeyError
        :param identifier: An integer required to identify node
        :return: Node (or raises exception)
        """
        for node in self.nodes:
            if node.identifier == identifier:
                return node

        raise KeyError("No node with such identifier")

    def __getitem__(self, identifier):
        """
        Alternative form of get_node_by_id :meth:`models.datatree.get_node_by_id`
        Example:
            print(block_tree[id].data)
        :param identifier: An integer required to identify node
        :return: Node (or raises exception)
        """
        return self.get_node_by_id(identifier)

    def __bool__(self):
        return bool(self.nodes)

    def size(self) -> int:
        """
        Returns amount of nodes
        :return:
        """
        return len(self.nodes)

    def __len__(self):
        return self.size()

    def to_id_adjacency_dict(self) -> Dict[int, Tuple[int]]:
        """
        Convert to adjacency dict where key is node id and value is tuple of neighbours ids
        Example:
            {7: (1, 5, 3), 3: (7,), 4: (5,), 1: (7, 6), 6: (1,), 5: (7, 4)}
            is
             .-7-.
            /  |  \
            1  5  3
            |  |
            6  4

        :return: Dict where key is node id and value is tuple of neighbour ids
        """
        result: Dict[int, Tuple[int]] = dict()
        for node in self.nodes:
            key = node.identifier
            values = tuple(neighbour.identifier for neighbour in node.neighbours)
            result[key] = values
        return result

    @classmethod
    def from_id_adjacency_dict(cls, adj_dict: Dict[int, Tuple[int]]):
        """
        Build DataTree from adjacency dict (see :meth:`models.datatree.to_id_adjacency_dict`)
        :param adj_dict:
        :return:
        """
        # create nodes without any neighbours
        node_by_id: Dict[int, DataNode] = {identifier: DataNode(identifier, None, []) for identifier in adj_dict.keys()}

        # Add an edge between nay pair of neighbours
        for node_id, neighbours_ids in adj_dict.items():
            node = node_by_id[node_id]
            for neighbour_id in neighbours_ids:
                neighbour = node_by_id[neighbour_id]
                # Already added
                if neighbour in node.neighbours:
                    continue
                node.neighbours.append(neighbour)
                neighbour.neighbours.append(node)

        # Copy values into block_tree object
        tree_obj = cls()
        for node in node_by_id.values():
            if node in tree_obj.nodes:
                continue
            tree_obj.nodes.append(node)
        return tree_obj

    def add(self, ancestor_id: Optional[int], new_id: int) -> None:
        """
        Adds Node to block_tree and makes an edge between new node and node with specified ancestor id.
        If :param ancestor_id: is None, attempts to add a root
        :raise ValueError: if attempts to add second root;
        :raise KeyError: if attempts to add second node with specified id
        :param ancestor_id: Ancestor nodes' identifier
        :param new_id: New node id
        :return:
        """
        if ancestor_id is None:
            # Adding root
            if self.nodes:
                raise ValueError("Can't add second root")
            else:
                self.nodes.append(DataNode(new_id, None, []))
        else:
            try:
                # Raises KeyError if nodes have already got a node with such id
                self.get_node_by_id(new_id)
                raise KeyError("Node with such identifier is present")
            except KeyError:
                # Adding node
                ancestor_node = self.get_node_by_id(ancestor_id)
                new_node = DataNode(new_id, None, [ancestor_node])
                ancestor_node.neighbours.append(new_node)
                self.nodes.append(new_node)

    @classmethod
    def random(cls, tree_size: int, root_id: Optional[int] = None):
        """
        Builds random block_tree with specified size. Root identifier is specified
        Uses :func`random.getrandbits` to generate random identifiers with RANDOM_ID_BITS size.
        Uses :func`random.choice` to choose random ancestor
        Uses :func`random.shuffle` to shuffle all nodes after building
        :param tree_size: Size of the block_tree
        :param root_id: Specified root identifier
        :return: random block_tree object
        """
        if tree_size < 0:
            raise ValueError("Tree size can't be negative")

        tree_obj = cls()
        if tree_size == 0:
            # block_tree is empty
            return tree_obj

        # list of used identifiers
        used_ids: List[int] = list()

        # adding root
        if root_id is None:
            r = getrandbits(RANDOM_ID_BITS)
        else:
            r = root_id
        tree_obj.add(None, r)
        used_ids.append(r)

        # adding random nodes
        for _ in range(tree_size - 1):
            # generate random not used id
            while r in used_ids:
                r = getrandbits(RANDOM_ID_BITS)

            # choose random ancestor id from used
            ancestor_id = choice(used_ids)
            tree_obj.add(ancestor_id, r)
            used_ids.append(r)

        # By default, appends to nodes, so need to shuffle
        shuffle(tree_obj.nodes)

        return tree_obj

    def for_each_node(self, root_id: int, func: Callable[[DataNode], Any]) -> List[Any]:
        """
        Uses BFS to iterate over all Nodes from root in ascending ids order and call function for each node
        :param root_id: An integer to identify a root and start BFS
        :param func: Function that argument is DataNode
        :return: List of function result for each node
        """
        root_node = self.get_node_by_id(root_id)

        results = list()

        # BFS queue
        queue = SimpleQueue()
        # To check if Node is visited or not
        in_queue: DefaultDict[int, bool] = defaultdict()

        # Put root in queue and mark as `will visit`
        queue.put(root_node)
        in_queue[root_node.identifier] = True

        while not queue.empty():
            cur_node = queue.get()
            cur_node_neighbours = cur_node.neighbours
            sorted_cur_node_neighbours = sorted(cur_node_neighbours, key=lambda node: node.identifier)

            results.append(func(cur_node))

            for neighbour in sorted_cur_node_neighbours:
                if not in_queue[neighbour.identifier]:
                    queue.put(neighbour)
                    in_queue[neighbour.identifier] = True
        return results

    def get_ids(self) -> List[int]:
        """
        Print all ids
        :return:
        """
        return [node.identifier for node in self.nodes]

    def get_tree_ids(self, root_id: int) -> List[int]:
        """
        Get list of all ids in BFS order
        :param root_id:
        :return:
        """
        results: List[int] = self.for_each_node(root_id, lambda node: node.identifier)
        return results

    def get_data(self, root_id: int) -> List[int]:
        """
        Get data in BFS order
        :param root_id:
        :return:
        """
        results = self.for_each_node(root_id, lambda node: node.data)
        return results

    def write_data(self, root_id: int, inp: List[int]) -> None:
        """
        Write data to each Node in BFS order
        :param root_id:
        :param inp: Input list
        :return:
        """
        assert len(inp) == len(self.nodes)

        inp_idx = 0

        def write_to_node(node: DataNode) -> None:
            nonlocal inp_idx
            node.data = inp[inp_idx]
            inp_idx += 1

        self.for_each_node(root_id, write_to_node)
