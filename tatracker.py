class Student:
    __slots__ = ('name', 'confusion', 'prev', 'next', 'heaploc')

    def __init__(self, name, conf):
        self.name = name
        self.confusion = conf
        self.next = None
        self.prev = None
        self.heaploc = -1

    def __str__(self):
        return self.name


class OliverQueue:
    __slots__ = ('head', 'tail')

    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, item):
        """
        Inserts an item into the tail of the queue.
        :param item: The item to be inserted
        :return: None
        """
        if self.head is None:
            self.head = item
        else:
            item.prev = self.tail
            self.tail.next = item
        self.tail = item

    def remove(self):
        """
        Removes an item from the head and returns it.
        :return: The item at the head.
        """
        if self.head is None:
            return
        rv = self.head
        self.head = self.head.next
        self.head.prev = None
        if self.head is None:
            self.tail = None
        return rv

    def removenode(self, stu):
        """
        Removes a node from queue.
        :param stu: The node to be removed.
        :return: None
        """
        if stu == self.head:
            self.remove()
        elif stu == self.tail:
            self.tail = stu.prev
            self.tail = None
        else:
            stu.prev.next = stu.next
            stu.next.prev = stu.prev

    def remaining(self):
        if self.head is None:
            print('None')
        else:
            self.__remaining(self.head)

    def __remaining(self, stu):
        if stu is None:
            return
        else:
            print(stu.name)
            self.__remaining(stu.next)


class ColleenHeap:
    __slots__ = ('list', 'size')

    def __init__(self):
        self.list = []
        self.size = 0

    def insert(self, item):
        """
        Inserts a value into the heap.
        :param item: the student to be inserted.
        :return: None
        """
        if self.size < len(self.list):
            self.list[self.size] = item
        else:
            self.list.append(item)
        item.heaploc = self.size
        self.size += 1
        self.__bubbleup(self.size-1)

    def __bubbleup(self, i):
        """
        Compares the heap value at the index with its parent.
        :param i: The child's index.
        :return: None
        """
        parent = (i - 1) // 2
        if i == 0 or self.list[i].confusion < self.list[parent].confusion:
            return
        else:
            self.list[i].heaploc = parent
            self.list[parent].heaploc = i
            self.list[i], self.list[parent] = self.list[parent], self.list[i]
            self.__bubbleup(parent)
        return parent

    def removenode(self, i):
        """
        Removes the student with the index.
        :param i: The index of the node to be removed.
        :return: None
        """
        self.size -= 1
        self.list[i] = self.list[self.size]
        self.list[i].heaploc = i
        self.__bubbledown(i)

    def remove(self):
        """
        Removes the student with the most confusion.
        :return: The student with the most confusion.
        """
        mostconfused = self.list[0]
        self.size -= 1
        self.list[0] = self.list[self.size]
        self.list[0].heaploc = 0
        self.__bubbledown(0)
        return mostconfused

    def __bubbledown(self, i):
        """
        Exchanges the heap node at the index with its two children to find the smallest.
        :param i: The node index.
        :return: None
        """
        large = self.__largest(i)
        if large == i:
            return None
        else:
            self.list[i].heaploc = large
            self.list[large].heaploc = i
            self.list[i], self.list[large] = self.list[large], self.list[i]
            self.__bubbledown(large)

    def __largest(self, i):
        """
        Compares the value with the largest value amongst its children.
        :param i: The index.
        :return: The largest value's index.
        """
        child1 = i * 2 + 1
        child2 = i * 2 + 2
        if child1 >= self.size:
            return i
        if child2 >= self.size:
            if self.list[i].confusion < self.list[child1].confusion:
                return child1
            else:
                return i
        if self.list[child1].confusion > self.list[i].confusion:
            if self.list[child1].confusion > self.list[child2].confusion:
                return child1
            else:
                return child2
        elif self.list[child2].confusion > self.list[i].confusion:
            return child2
        else:
            return i


def file_check(file, perm):
    try:
        f = open(file, perm)
        return f
    except FileNotFoundError:
        print("File", file, "does not exist...")
        exit()


def printhelp(s):
    print(s, 'is looking for help!')


def printhelping(s, ta):
    print(ta, 'helping', s)


def start(file):
    oq = OliverQueue()
    ch = ColleenHeap()
    for line in file:
        line.strip()
        l = line.split(" ")
        if l[1] == 'ready\n':
            if l[0] == 'Oliver':
                stu = oq.remove()
                ch.removenode(stu.heaploc)
                print('Oliver is helping', stu.name)
            elif l[0] == 'Colleen':
                stu = ch.remove()
                oq.removenode(stu)
                print('Colleen is helping', stu.name)
        else:
            l[1] = int(l[1][:len(l[1]) - 1])
            s = Student(l[0], l[1])
            oq.insert(s)
            ch.insert(s)
            printhelp(s)
    print('Students who have not been helped:')
    oq.remaining()


def main():
    f = input('Enter the file name: ')
    file = file_check(f, 'r')
    start(file)

if __name__ == '__main__':
    main()
