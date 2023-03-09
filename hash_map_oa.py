# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key-value pair to the hash map. Resizes the hash map if the load factor is greater than or equal to 0.5.
        """
        # Check if the load factor is greater than or equal to 0.5
        if self.table_load() >= 0.5:
            # Double the capacity of the hash map
            self.resize_table(self._capacity * 2)

        # Compute the index of the bucket where the entry should be inserted
        index = self._hash_function(key) % self._capacity

        # Iterate over the buckets using quadratic probing to find an empty slot
        i = 0
        while i < self._capacity:
            # Compute the index of the next bucket to check
            next_index = (index + i ** 2) % self._capacity

            # Get the entry at the current bucket
            entry = self._buckets[next_index]

            if entry is None or entry.is_tombstone:
                # If the current bucket is empty or has a deleted entry, insert the new entry
                self._buckets[next_index] = HashEntry(key, value)
                self._size += 1
                return
            elif entry.key == key:
                # If the current bucket has an entry with the same key, update its value
                entry.value = value
                return

            i += 1

        # If we have iterated over all the buckets without finding an empty slot,
        # we need to resize the hash map
        self.resize_table(self._capacity * 2)

        # Insert the new entry
        index = self._hash_function(key) % self._capacity
        i = 0
        while i < self._capacity:
            next_index = (index + i ** 2) % self._capacity
            entry = self._buckets[next_index]
            if entry is None or entry.is_tombstone:
                self._buckets[next_index] = HashEntry(key, value)
                self._size += 1
                return
            i += 1

    def table_load(self) -> float:
        """
        Returns the HashMap's load factor
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash map.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash map to the new_capacity
        """
        if new_capacity < self.get_size():
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        for i in range(self._buckets.length()):
            entry = self._buckets[i]
            if entry and not entry.is_tombstone:
                hash_value = self._hash_function(entry.key) % new_capacity
                if not new_buckets[hash_value]:
                    new_buckets[hash_value] = entry
                else:
                    # quadratic probing to find new index
                    i = 1
                    while True:
                        new_index = (hash_value + i * i) % new_capacity
                        if not new_buckets[new_index]:
                            new_buckets[new_index] = entry
                            break
                        i += 1

        self._capacity = new_capacity
        self._buckets = new_buckets

        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key in the hash map, or None if the key is not in the hash map.
        """
        # Compute the index of the bucket where the entry with the given key should be located
        index = self._hash_function(key) % self._capacity

        # Iterate over the buckets using quadratic probing to find the entry with the given key
        i = 0
        while i < self._capacity:
            # Compute the index of the next bucket to check
            next_index = (index + i ** 2) % self._capacity

            # Get the entry at the current bucket
            entry = self._buckets[next_index]

            if entry is None:
                # If the current bucket is empty, the key is not in the map
                return None
            elif entry.key == key and not entry.is_tombstone:
                # If the current bucket has an entry with the same key, return its value
                return entry.value

            i += 1

        # If we have iterated over all the buckets without finding the entry with the given key,
        # the key is not in the map
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, False otherwise.
        """
        return self.get(key) != None

    def remove(self, key: str) -> None:
        """
        Removes the key-value pair with the given key from the hash map.
        """
        # Compute the index of the bucket where the entry should be located
        index = self._hash_function(key) % self._capacity

        # Iterate over the buckets using quadratic probing to find the entry with the given key
        i = 0
        while i < self._capacity:
            # Compute the index of the next bucket to check
            next_index = (index + i ** 2) % self._capacity

            # Get the entry at the current bucket
            entry = self._buckets[next_index]

            if entry is None:
                # If the current bucket is empty, the entry is not in the hash map
                return
            elif entry.key == key:
                # If the current bucket has an entry with the same key, remove it
                entry.is_tombstone = True
                self._size -= 1
                return

            i += 1

    def clear(self) -> None:
        """
        Removes all key-value pairs from the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all key-value pairs stored in the hash map.
        """
        da = DynamicArray()
        for entry in self:
            da.append((entry.key, entry.value))

        return da

    def __iter__(self):
        """
        Returns an iterator object that can iterate over all entries in the hash map.
        """
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            if bucket is not None and not bucket.is_tombstone:
                yield bucket

    def __next__(self):
        """
        Return the next key in the iteration
        """
        if self._next_index is None:
            self._next_index = 0

        while self._next_index < self._capacity:
            bucket = self._buckets[self._next_index]
            self._next_index += 1

            if bucket is not None and not bucket.is_tombstone:
                return bucket

        self._next_index = None
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
