from models.datatree import DataTree
from typing import Dict, Tuple, List

BLOCK_SIZE = 16


class TreeSubCipher:
    block_tree: DataTree
    encryption_key: int

    def __init__(self, key: int) -> None:
        self.block_tree = DataTree.random(BLOCK_SIZE, key)
        self.encryption_key = key

    @classmethod
    def random(cls, key: int):
        return cls(key)

    @classmethod
    def from_id_adjacency_dict(cls, adj_dict: Dict[int, Tuple[int]], key: int):
        tree_sub_cipher = cls(key)
        tree_sub_cipher.block_tree = DataTree.from_id_adjacency_dict(adj_dict)

        return tree_sub_cipher

    @classmethod
    def from_tree(cls, tree: DataTree, key: int):
        tree_sub_cipher = cls(key)
        tree_sub_cipher.block_tree = tree
        return tree_sub_cipher

    def get_adjacency_dict(self):
        return self.block_tree.to_id_adjacency_dict()

    def get_tree(self):
        return self.get_adjacency_dict()

    def get_data(self):
        return self.block_tree.get_data(self.encryption_key)

    def encrypt(self, plain_data: List[int]):
        pass

    def decrypt(self, encrypted_data: List[int]):
        pass
