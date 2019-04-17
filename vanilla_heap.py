import numpy as np

class VanillaHeap ():

    def insert (self, A, key):
        A.append(-float('inf'))
        return self.reduce_key(A, len(A)-1, key)

    def extract_min (self, A):

        if len(A) <= 1:
            return None, 'Empty Heap'

        min = A[1]
        A[1] = A[-1]
        A = A[0:-1]
        self.min_heapify(A, 1)
        return min, A

    def reduce_key (self, A, i, key):
        A[i] = key
        if A[i] < key:
            return A
        while i > 1 and A[self.parent(A,i)] > A[i]:
            A = self.swap(A, i, self.parent(A,i))
            i = self.parent(A,i)
        return A

    def delete (self, node):
        pass

    def parent (self, A, i):
        if i == 1: return None
        return int(np.floor(i/2))

    def left (self, A, i):
        if 2 * i  <= len(A): return 2 * i
        return None

    def right (self, A, i):
        if 2 * i + 1 <= len(A): return 2 * i + 1
        return None

    def min_heapify (self, A, i):

        l = self.left(A, i)
        r = self.right(A, i)
        smallest = None

        if l and l < len(A) and A[l] < A[i]:
            smallest = l
        else:
            smallest = i

        if r and r < len(A) and A[r] < A[smallest]:
            smallest = r

        if smallest != i:
            A = self.swap(A, i, smallest)
            self.min_heapify(A, smallest)

        return A

    def swap (self, A, i, j):
        temp = A[i]
        A[i] = A[j]
        A[j] = temp
        return A

    def build_min_heap (self, A):
        for i in reversed(range(1,len(A))):
            A = self.min_heapify(A, i)
        return A

h = VanillaHeap()
array = [None, 5,4,3,2,1]
a = h.build_min_heap(array)
print('fin: ', a)
a = h.insert(a, -10)
print(a)
