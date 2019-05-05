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

    def add(self, item):
        self.length += 1
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def addend(self, item):
        current = self.head
        count = self.length
        temp = Node(item)
        while count > 1:
           # print(current.getData())
            current = current.getNext()
            count -= 1
        current.setNext(temp)
    #    print("current get data " + str(current.getData()))
    #   print("current get next " + str(current.getNext()))

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
                # print(current.getNext())
            else:
                current = current.getNext()

        return found

    def printlist(self):
        current = self.head
        while current != None:
            print(current.getData())
            current = current.getNext()

mylist = Task1List()
mylist.add(1)
mylist.add(2)
mylist.add(3)
mylist.addend(4)
print('test')
mylist.printlist()
