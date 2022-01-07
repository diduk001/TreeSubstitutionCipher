# Tree Substitution Cipher


## Generation Algorithm:
1. Generate random tree.
   Tree nodes contain ID, Neighbours and Data (an integer)
2. Key is root's ID

## To encrypt:
1. Write data in nodes in BFS order with sorting by IDs
2. Encrypted is dict where key is ID and value is Node's data

## To decrypt:
1. Write data in nodes by ids
2. Read in BFS order with sorting by IDs

### For encryption and decryption example see main.py