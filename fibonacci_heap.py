import numpy as np

class Node ():
    def __init__ (self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.children = []
        self.degree = 0
        self.mark = False

    # TODO: clean up this mess!
    def __str__ (self):
        string = ''
        string += 'key: ' + str(self.key)
        if self.parent:
            string += '\tparent: ' + str(self.parent.key)
        else:
            string += '\tparent: ' + str(None)
        string += '\tchildren: ' + str(len(self.children))
        string += '\tdegree: ' + str(self.degree)
        string += '\tmarked: ' + str(self.mark)
        return string

class FibonacciHeap ():

    def __init__ (self):
        self.create()

    # create an empty heap!
    def create (self):
        self.roots = []
        self.min_key = None
        self.total_nodes = 0

    # insert node by creating a singleton heap and mergin it with the root list
    def insert (self, key, value):
        new_heap = Node(key, value)
        self.roots = self.merge(self.roots, [new_heap])
        self.update_min()
        self.total_nodes += 1
        return new_heap

    # merge two heaps!
    def merge (self, h1, h2):
        if h1 is None: h1 = []
        if h2 is None: h2 = []
        if type(h1) is not type([]):
            h1 = [h1]
        if type(h2) is not type([]):
            h2 = [h2]
        return h1 + h2

    # cycle through root nodes to determine the new min key
    def update_min(self):
        min_tree_index = None
        min_tree_key = float("inf")
        for i, tree in enumerate(self.roots):
            if tree.key < min_tree_key:
                min_tree_key = tree.key
                min_tree_index = i
        self.min_key = self.roots[min_tree_index]

    # return the min key without extracting it
    def peak (self):
        return self.min_key

    # add the heap with the larger key as a child to the other in order to
    # maintain the heap property
    def link (self, h1, h2):

        # determine which tree will become the parent and child
        parent = h1 if h1.key < h2.key else h2
        child = h1 if parent != h1 else h2

        # update child's parent pointer and merge the child with the parent's children
        child.parent = parent
        parent.children = self.merge(parent.children, child)

        # increase the degree of the parent tree and remove the child from
        # the roots list
        parent.degree += 1
        self.roots.remove(child)

        return parent

    def extract_min (self):

        # update heaps total nodes
        self.total_nodes -= 1

        # check for empty heap and heap of length 1
        if not self.roots:
            return self.create()

        # save min key to return later and remove node from heap
        min = self.min_key
        self.roots.remove(min)

        # merge min node's children with root list
        if len(min.children) > 0:
            min.children[0].parent = None
            self.roots = self.merge(self.roots, min.children)

        # consolidate heap and update the min key
        self.consolidate()
        self.update_min()

        return min

    # link trees until each has a unique degree (# of children)
    def consolidate (self):

        heap_degrees = [None for _ in range(int(np.log2(self.total_nodes)) + 1)]
        idx = 0 # keep track of tree under consideration
        node = self.roots[idx] # first node to be considered

        while 1:

            # degree of node under consideration
            degree = node.degree

            # enter statement if there already exists a tree of the same degree
            if heap_degrees[degree]:

                # break loop if all trees have unique degrees
                if heap_degrees[degree] == node:
                    break

                # link trees with same degree and erase trees from heap_degrees
                node = self.link(node, heap_degrees[degree])
                heap_degrees[degree] = None

            else:

                # record that tree has a uniqe degree so far
                heap_degrees[node.degree] = node

                # increment node to next node in list (funky modulo stuff to make it happen!)
                node = self.roots[(self.roots.index(node)+1)%len(self.roots)]

    # decrease the key of a node and restructure using cascading cuts
    def decrease_key(self, node, new_key):

        # update key!
        node.key = new_key

        # check if node is in root list
        if (node.parent == None):
            if (self.min_key.key > node.key):
                self.min_key = node
            return

        # check if heap condition isn't violated
        if (node.parent.key < node.key):
            return

        # remove node, add node to root list and update min
        parent = node.parent
        node.parent = None
        parent.children.remove(node)
        self.roots = self.merge(self.roots, node)
        self.update_min() # TODO: just do the comparison, it'll be quicker

        # perform cascading cuts to keep trees fairly binomial tree shaped
        self.cascading_cuts(parent)

    # restructure tree
    def cascading_cuts(self, node):

        # decrease degree of parent that lost a child!
        node.degree -= 1

        # stop the cascade if the node is a root
        if node.parent is None:
            return

        # if node is already marked, then this is the second time a child has
        # been removed. Cut out this subtree and make it a root.
        if node.mark:
            node.parent.children.remove(node)
            node.mark = False
            self.merge(self.roots, node)
            self.cascading_cuts(parent.node)
        else:

            # mark node true if this is the first time a child has been removed
            node.mark = True

    # delete node by decreasing its key to neg. infinity and extracting the min
    def delete(self, node):
        self.decrease_key(node, -float('inf'))
        self.extract_min()

    # print the heaps roots
    def print_roots (self):
        print('\nprinting roots...')
        if self.roots is None or len(self.roots) == 0:
            return print('Heap is empty')
        for i in self.roots:
            print(i)

    # print the entire heap
    def print_heap(self, root, depth):
        if not self.roots:
            return print('heap is empty')
        for i in root:
            print('depth: ', depth, '\t', i)
            if i.children:
                self.print_heap(i.children, depth+1)

# NOTE: More robust testing to come!
fh = FibonacciHeap()

# insert eleven values
for i in range(8):
    fh.insert(i, i)
node0 = fh.insert(8, 8)
node1 = fh.insert(9, 9)
node2 = fh.insert(10, 10)

# couple operations ...
fh.extract_min()
fh.decrease_key(node1, -1)
fh.delete(node0)

print('\nprinting heap...')
fh.print_heap(fh.roots, 0)

print('\nheap min: ', fh.peak())
