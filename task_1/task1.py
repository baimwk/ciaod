class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class Task1List:
    def __init__(self):
        self.head = None
        self.length = 0

    def addBefore(self, before, value):
        temp = Node(value)
        addend = self.head
        if self.length == 0:
            temp.setNext(self.head)
            self.head = temp
        else:
            if self.search(before):
                temp.setNext(self.head)
                self.head = temp
            else:
                count = self.length
                while count > 1:
                    addend = addend.getNext()
                    count -= 1
                addend.setNext(temp)
        self.length += 1
        self.printlist()

    def printlist(self):
        if self.head is not None:
            current = self.head
            print("[", end=' ')
            while current is not None:
                print(current.getData(), end=' ')
                current = current.getNext()
            print("]")
        else:
            print("Массив пуст")

    def remove(self, num):
        if self.length > 0 and num < self.length:
            current = self.head
            previous = None
            count = num
            while count > 0:
                previous = current
                current = current.getNext()
                count -= 1
            self.length -= 1
            if previous is None:
                self.head = current.getNext()
            else:
                previous.setNext(current.getNext())
        else:
            if self.length == 0:
                print('Из массива нечего удалить, он пуст')
            else:
                print("В массиве всего " + str(self.length) + " элемента(ов)")
        self.printlist()

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found


print('mylist:')
mylist = Task1List()
mylist.addBefore(1, 2)
mylist.addBefore(2, 1)
mylist.addBefore(4, 'string')
mylist.addBefore(4, 4)
print(mylist.search('string'))
mylist.remove(3)
print(mylist.search(4))
mylist.remove(25)

print('empty list:')
myemptylist = Task1List()
myemptylist.remove(1)
print(mylist.search(376))
