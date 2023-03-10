# Name:
# OSU Email:
# Course: CS261
# Assignment:
# Due Date:
# Description:


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
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
        Takes as parameters a key and a value. Performs hash function with key and determines index. If the key already
        exists it is replaced by the new key-value pair. If the index is already filled with another key, quadratic
        probing will be used until either the key matches the key of an entry, in which case it will be updated with
        the new value, or until an empty index is found, in which case the new key-value pair is added as a hash entry.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        da = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity

        if da.get_at_index(index) is None or da.get_at_index(index).is_tombstone is True:
            da.set_at_index(index, HashEntry(key, value))
            self._size += 1
        else:
            if da.get_at_index(index).key == key:
                da.get_at_index(index).value = value
            else:
                probe = 1
                new_index = (index + probe**2) % self._capacity
                while da.get_at_index(new_index) is not None and da.get_at_index(new_index).is_tombstone is False:
                    if da.get_at_index(new_index).key == key:
                        da.get_at_index(new_index).value = value
                        return
                    else:
                        probe += 1
                        new_index = (index + probe**2) % self._capacity

                da.set_at_index(new_index, HashEntry(key, value))
                self._size += 1

    def table_load(self) -> float:
        """
        Takes no parameters. Calculates and returns the load factor for the table.
        """
        da = self._buckets
        loop_counter = 0
        element_counter = 0

        while loop_counter < da.length():
            if da.get_at_index(loop_counter) is not None and da.get_at_index(loop_counter).is_tombstone is False:
                element_counter += 1
            loop_counter += 1

        load_factor = element_counter/self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Counts and returns the number of empty indices in the dynamic array.
        """
        loop_counter = 0
        bucket_counter = 0
        da = self._buckets

        while loop_counter < da.length():
            if da.get_at_index(loop_counter) is None or da.get_at_index(loop_counter).is_tombstone == True:
                bucket_counter += 1
            loop_counter += 1

        return bucket_counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes as a parameter the new capacity for the dynamic array. Resizes the array to the new capacity and rehashes
        and transfers the pre-existing data into the new array. Assigns the new array to the current hash table and
        updates the capacity.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1:
            return

        old_da = self._buckets
        old_cap = self._capacity
        new_hm = HashMap(new_capacity, self._hash_function)
        new_da = new_hm._buckets
        self._capacity = new_capacity
        self._buckets = new_da
        self._size = 0
        counter = 0

        while counter < old_cap:
            hash_entry = old_da.get_at_index(counter)
            if hash_entry is not None and hash_entry.is_tombstone is False:
                key = hash_entry.key
                value = hash_entry.value
                self.put(key, value)
            counter += 1

    def get(self, key: str) -> object:
        """
        Takes as a parameter a key. Searches at the hashed index, then at the indices determined by quadratic probing
        for the key. If the key is found, returns the value of the hash entry. Otherwise, returns None.
        """
        da = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity
        if da.get_at_index(index) is None:
            return None
        else:
            if da.get_at_index(index).key == key and da.get_at_index(index).is_tombstone is False:
                return da.get_at_index(index).value
            else:
                probe = 1
                new_index = (index + probe**2) % self._capacity
                while da.get_at_index(new_index) is not None:
                    if da.get_at_index(new_index).is_tombstone is False:
                        if da.get_at_index(new_index).key == key:
                            return da.get_at_index(new_index).value
                    probe += 1
                    new_index = (index + probe**2) % self._capacity

                return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter. Searches the table for the key. If the key exists in the table, returns True.
        Otherwise, returns False.
        """
        da = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity
        if da.get_at_index(index) is None:
            return False
        else:
            if da.get_at_index(index).key == key and da.get_at_index(index).is_tombstone is False:
                return True
            else:
                probe = 1
                new_index = (index + probe ** 2) % self._capacity
                while da.get_at_index(new_index) is not None:
                    if da.get_at_index(new_index).is_tombstone is False:
                        if da.get_at_index(new_index).key == key:
                            return True
                    probe += 1
                    new_index = (index + probe ** 2) % self._capacity

                return False

    def remove(self, key: str) -> None:
        """
        Takes as a parameter a key. Searches table for key and removes the hash entry if it exists.
        """
        da = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity

        if da.get_at_index(index) is None:
            return
        else:
            if da.get_at_index(index).key == key and da.get_at_index(index).is_tombstone is False:
                da.get_at_index(index).is_tombstone = True
                self._size -= 1
                return
            else:
                probe = 1
                new_index = (index + probe ** 2) % self._capacity
                while da.get_at_index(new_index) is not None:
                    if da.get_at_index(new_index).is_tombstone is False:
                        if da.get_at_index(new_index).key == key:
                            da.get_at_index(new_index).is_tombstone = True
                            self._size -= 1
                            return
                    probe += 1
                    new_index = (index + probe ** 2) % self._capacity

    def clear(self) -> None:
        """
        Takes no parameters. Clears the table.
        """
        new_hm = HashMap(self._capacity, self._hash_function)
        new_da = new_hm._buckets
        self._buckets = new_da
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters. Iterates through hash map and adds keys to new dynamic array, Returns the new dynamic array
        containing all the keys in the hash map.
        """
        new_da = DynamicArray()
        da = self._buckets
        loop_counter = 0

        while loop_counter < self._capacity:
            if da.get_at_index(loop_counter) is not None and da.get_at_index(loop_counter).is_tombstone is False:
                key = da.get_at_index(loop_counter).key
                new_da.append(key)
            loop_counter += 1

        return new_da

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
