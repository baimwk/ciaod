class MyHashTable:
    def __init__(self):  # имя конструктора класса
        self.size = 11
        self.slots = [None] * self.size  # ключи элементов
        self.data = [None] * self.size  # значения

    def put(self, key, data):  # Добавляет новую пару ключ-значение в отображение. Если ключ имеется, то заменяет старый
        hashvalue = self.hashfunction(key, len(self.slots))

        if self.slots[hashvalue] is None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data  # replace
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))
                while self.slots[nextslot] is not None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot, len(self.slots))

                if self.slots[nextslot] is None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data  # replace

    def hashfunction(self, key, size):  # простой метод остатков
        return key % size

    def rehash(self, oldhash, size):  # линейное пробивание на 1
        return (oldhash + 1) % size

    def get(self, key):  # Принимает ключ, возвращает соответствующее ему значение из коллекции или None
        startslot = self.hashfunction(key, len(self.slots))

        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] is not None and not found and not stop:
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position, len(self.slots))
                if position == startslot:
                    stop = True
        return data

    def printtable(self):
        for i in range(0, self.size, 1):
            print(self.slots[i], " ", self.data[i])


H = MyHashTable()
H.put(56, 'cat')
H.put(57, 'dog')
H.put(58, 'h')
H.put(65, 'ggg')
print(H.slots)
print(H.data)
H.printtable()
