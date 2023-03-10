# Name:
# OSU Email:
# Course: CS261 -
# Assignment: Assignment 6 -
# Due Date:
# Description


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        exists it is replaced by the new key-value pair. Otherwise, the key-value pair is added.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        da = self._buckets
        cur_ll = da.get_at_index(index)

        if cur_ll.contains(key):
            cur_ll.remove(key)
            cur_ll.insert(key, value)
        else:
            cur_ll.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Counts and returns the number of empty indices in the dynamic array.
        """
        loop_counter = 0
        bucket_counter = 0
        da = self._buckets
        while loop_counter < self._capacity:
            cur_ll = da.get_at_index(loop_counter)
            if cur_ll.length() == 0:
                bucket_counter += 1

            loop_counter += 1

        return bucket_counter

    def table_load(self) -> float:
        """
        Takes no parameters. Calculates and returns the load factor for the table.
        """
        loop_counter = 0
        node_counter = 0
        da = self._buckets

        while loop_counter < self._capacity:
            cur_ll = da.get_at_index(loop_counter)
            node_counter += cur_ll.length()
            loop_counter += 1

        load_factor = node_counter/self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Takes no parameters. Clears the table.
        """
        new_hm = HashMap(self._capacity, self._hash_function)
        new_da = new_hm._buckets
        self._buckets = new_da
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes as a parameter the new capacity for the dynamic array. Resizes the array to the new capacity and rehashes
        and transfers the pre-existing data into the new array. Assigns the new array to the current hash table and
        updates the capacity.
        """
        if new_capacity < 1:
            return

        old_cap = self._capacity
        da_counter = 0
        ll_counter = 0
        da = self._buckets
        new_hm = HashMap(new_capacity, self._hash_function)
        new_da = new_hm._buckets

        while da_counter < old_cap:
            cur_ll = da.get_at_index(da_counter)
            ll_iter = cur_ll.__iter__()
            while ll_counter < cur_ll.length():
                cur_node = ll_iter.__next__()
                cur_key = cur_node.key
                cur_val = cur_node.value
                #hash = self._hash_function(cur_key)
                #index = hash % new_capacity
                new_hm.put(cur_key, cur_val)
                ll_counter += 1

            ll_counter = 0
            da_counter += 1

        self._capacity = new_capacity
        self._buckets = new_da

    def get(self, key: str) -> object:
        """
        Takes as a parameter a key. Searches the linked list at the appropriate index for the key. If the key is there,
        returns the value of the node. Otherwise, returns None.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        da = self._buckets
        counter = 0

        cur_ll = da.get_at_index(index)
        if cur_ll.contains(key) is not None:
            ll_iter = cur_ll.__iter__()
            while counter < cur_ll.length():
                cur_node = ll_iter.__next__()
                if cur_node.key == key:
                    return cur_node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter. Searches the table for the key. If the key exists in the table, returns True.
        Otherwise, returns False.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        cur_ll = self._buckets.get_at_index(index)
        cur_node = cur_ll.contains(key)
        if cur_node is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Takes as a parameter a key. Searches table for key and removes the node if it exists.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        cur_ll = self._buckets.get_at_index(index)
        if cur_ll.remove(key) is True:
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters. Iterates through hash map and adds keys to new dynamic array, Returns the new dynamic array
        containing all the keys in the hash map.
        """
        new_da = DynamicArray()
        da = self._buckets
        da_counter = 0
        ll_counter = 0

        while da_counter < self._capacity:
            cur_ll = da.get_at_index(da_counter)
            ll_iter = cur_ll.__iter__()

            while ll_counter < cur_ll.length():
                cur_node = ll_iter.__next__()
                cur_key = cur_node.key
                new_da.append(cur_key)
                ll_counter += 1

            ll_counter = 0
            da_counter += 1

        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes as a parameter a dynamic array of strings. Moves strings into hash map as keys with their frequencies as
    values and calculates max_val. Builds new DA with all keys whose values matches max_val. Returns a tuple with mode and frequency.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)
    max_val = 0
    counter = 0

    while counter < da.length():
        key = da.get_at_index(counter)
        if map.contains_key(key):
            value = map.get(key)
            value += 1
            map.put(key, value)
            if value > max_val:
                max_val = value
        else:
            value = 1
            map.put(key, value)
            if value > max_val:
                max_val = value
        counter += 1

    map_keys = map.get_keys()
    result_da = DynamicArray()
    counter = 0
    while counter < map_keys.length():
        key = map_keys.get_at_index(counter)
        cur_val = map.get(key)
        if cur_val == max_val:
            result_da.append(key)
        counter += 1

    return result_da, max_val


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

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

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load()),2)
    m.put('key1', 10)
    print(round(m.table_load()), 2)
    m.put('key2', 20)
    print(round(m.table_load()), 2)
    m.put('key1', 30)
    print(round(m.table_load()), 2)

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print((round(m.table_load(),2), m.get_size(), m.get_capacity()))

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
    m = HashMap(53  , hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1,6):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

        test_cases = (
            ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu",
            "Ubuntu", "Ubuntu"],
            ["one", "two", "three", "four", "five"],
            ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
            )

        for case in test_cases:
             da = DynamicArray(case)
             mode, frequency = find_mode(da)
             print(f"{da}\nMode : {mode}, Frequency: {frequency}\n")