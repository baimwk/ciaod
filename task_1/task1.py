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
        current = self.head
        addend = self.head
        found = False
        while current != None and not found:
            if current.getData() == before:
                found = True
            else:
                current = current.getNext()
        if self.length == 0:
            temp.setNext(self.head)
            self.head = temp
        else:
            if found:
                temp.setNext(self.head)
                self.head = temp
            if not found:
                count = self.length
                while count > 1:
                    addend = addend.getNext()
                    count -= 1
                addend.setNext(temp)
        self.length += 1

    def printlist(self):
        if self.head != None:
            current = self.head
            while current != None:
                print(current.getData())
                current = current.getNext()
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
            if previous == None:
               self.head = current.getNext()
            else:
               previous.setNext(current.getNext())
        else:
            if self.length == 0:
                print('Из массива нечего удалить, он пуст')
            else:
                print("В массиве всего " + str(self.length) + " элемента(ов)")


mylist = Task1List()
mylist.addBefore(1, 2)
mylist.addBefore(2, 1)
mylist.addBefore(4, 3)
mylist.addBefore(4, 4)
mylist.printlist()
mylist.remove(3)
mylist.remove(25)
mylist.printlist()

myemptylist = Task1List()
myemptylist.remove(1)
myemptylist.printlist()
