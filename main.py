import random  # for generating random key
from typing import Dict, Tuple, List  # for type hinting

from models.datatree import DataTree


class TreeSubCipher:
    """
    Substitution Cipher on tree Encryption System

    Generation Algorithm:
    1. Generate random tree (see :meth:`models.datatree.DataTree.random`).
       Tree nodes contain Identifiers, Neighbours and Data (an integer)
    2. Key is root's identifier

    To encrypt:
    1. Write data in nodes in BFS order with sorting by IDs (see :meth:`models.datatree.DataTree.for_each_node`)
    2. Encrypted is dict where key is ID and value is Node's data

    To decrypt:
    1. Write data in nodes by ids
    2. Read in BFS order with sorting by IDs
    """
    encryption_tree: DataTree
    encryption_key: int

    def __init__(self, size: int, key: int) -> None:
        """
        Builds random tree of specified size. See :meth:`models.datatree.DataTree.random`
        :param size: 
        :param key: 
        """
        self.tree = DataTree.random(size, key)
        self.encryption_key = key

    @classmethod
    def random(cls, sz: int, key: int):
        return cls(sz, key)

    @classmethod
    def from_id_adjacency_dict(cls, adj_dict: Dict[int, Tuple[int]], key: int):
        """
        Builds tree by specified adjacency dict and key
        :param adj_dict:
        :param key:
        :return:
        """
        tree_from_dict = DataTree.from_id_adjacency_dict(adj_dict)
        tree_sub_cipher = cls(tree_from_dict.size(), key)
        tree_sub_cipher.tree = tree_from_dict

        return tree_sub_cipher

    @classmethod
    def from_tree(cls, tree: DataTree, key: int):
        """
        Builds tree from DataTree object
        :param tree:
        :param key:
        :return:
        """
        tree_sub_cipher = cls(tree.size(), key)
        tree_sub_cipher.tree = tree
        return tree_sub_cipher

    def get_adjacency_dict(self):
        """
        Returns tree's adjacency dict.
        See :meth:`models.datatree.DataTree.to_id_adjacency_dict`
        :return:
        """
        return self.tree.to_id_adjacency_dict()

    def get_tree(self):
        return self.get_adjacency_dict()

    def get_data_dict(self) -> Dict[int, int]:
        """
        Returns data dict
        :return:
        """
        return self.tree.get_data_dict()

    def encrypt(self, plain_data: List[int]) -> Dict[int, int]:
        """
        Encrypts plain data
        :param plain_data:
        :return: Data dict (see :meth:`models.datatree.DataTree.get_data_dict`)
        """
        self.tree.write_data(self.encryption_key, plain_data)
        return self.get_data_dict()

    def decrypt(self, encrypted_data_dict: Dict[int, int]) -> List[int]:
        """
        Decrypts encrypted data
        :param encrypted_data_dict:
        :return: List of integerse - plain data
        """
        self.tree.write_by_data_dict(encrypted_data_dict)
        return self.tree.get_data(self.encryption_key)


if __name__ == '__main__':
    # Encrypt / decrypt message
    msg = list(b"Hello, World!")
    # Generate random key
    random_key = random.getrandbits(60)
    # Create tree for encryption and encrypt
    cipher_encrypt = TreeSubCipher(len(msg), random_key)
    cipher_encrypt.encrypt(msg)

    # Get encryption tree's parameters
    encryption_tree = cipher_encrypt.get_tree()
    encryption_data = cipher_encrypt.get_data_dict()

    # Decrypt and print
    cipher_decrypt = TreeSubCipher.from_id_adjacency_dict(encryption_tree, random_key)
    print(bytes(cipher_decrypt.decrypt(encryption_data)))
