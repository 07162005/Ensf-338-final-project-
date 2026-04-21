class HashMap:
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.table = []
        self.size = 0

        for _ in range(capacity):
            self.table.append([])   # each slot is a bucket (list)

    def _hash(self, key):
        hash_value = 0
        key = str(key)

        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.capacity

        return hash_value

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            stored_key, stored_value = bucket[i]
            if stored_key == key:
                bucket[i] = (key, value)   # update existing key
                return

        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for stored_key, stored_value in bucket:
            if stored_key == key:
                return stored_value

        return None

    def remove(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            stored_key, stored_value = bucket[i]
            if stored_key == key:
                bucket.pop(i)
                self.size -= 1
                return stored_value

        return None

    def contains_key(self, key):
        return self.get(key) is not None

    def keys(self):
        result = []

        for bucket in self.table:
            for stored_key, stored_value in bucket:
                result.append(stored_key)

        return result

    def values(self):
        result = []

        for bucket in self.table:
            for stored_key, stored_value in bucket:
                result.append(stored_value)

        return result

    def items(self):
        result = []

        for bucket in self.table:
            for stored_key, stored_value in bucket:
                result.append((stored_key, stored_value))

        return result

    def __len__(self):
        return self.size