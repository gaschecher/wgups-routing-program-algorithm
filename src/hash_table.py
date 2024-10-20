import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class HashTable:
    def __init__(self, size=40):
        # Initialize hash table with a fixed size and empty lists for each bucket.
        self.size = size
        self.table = [[] for _ in range(self.size)]
        logging.info(f"Initialized HashTable with size {size}")

    def _hash(self, key):
        # Compute the hash index for a given key.
        return hash(key) % self.size

    def insert(self, key, value):
        # Insert or update a key-value pair in the hash table.
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                logging.debug(f"Updated key {key} in HashTable")
                return
        self.table[index].append((key, value))
        logging.debug(f"Inserted new key-value pair {key}:{value} into HashTable")

    def lookup(self, key):
        # Search for a key in the hash table and return the associated value.
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                logging.debug(f"Lookup successful for key {key}")
                return item[1]
        logging.debug(f"Lookup failed for key {key}")
        return None

    def remove(self, key):
        # Remove a key-value pair from the hash table.
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                logging.debug(f"Removed key {key} from HashTable")
                return True
        logging.debug(f"Remove failed for key {key}: not found")
        return False

    def __str__(self):
        return "\n".join(str(item) for sublist in self.table for item in sublist)