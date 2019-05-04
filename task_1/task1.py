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
        self.length +=1
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
                #print(current.getNext())
            else:
                current = current.getNext()

        return found


mylist = Task1List()

mylist.add(2)
mylist.add('jkk')
mylist.add(34)
print(mylist.search(34))
print(mylist.search(35))
print(mylist.search('jkk'))
