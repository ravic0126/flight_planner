'''
Python Code to implement a heap with general comparison function
'''


def comp1(a, b):
    if a[0] < b[0] or a[0] == b[0] and a[1].flight_no < b[1].flight_no:
        return True
    else:
        return False
def comp2(a,b):
    if a[0] < b[0] or (a[0]==b[0] and a[1]<b[1]) or (a[0]==b[0] and a[1]==b[1] and a[2]<b[2]):
        return True
    else:
        return False
class Heap:
    '''
    Class to implement a heap with general comparison function
    '''

    def __init__(self, comparison_function, init_array=[]):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        self.comparator_function = comparison_function
        self.data = self.build_min_heap(init_array)

        pass

    def left(self, k):
        return 2 * k + 1

    def right(self, k):
        return 2 * k + 2

    def parent(self, k):
        return (k - 1) // 2

    def swap(self, A, l, r):
        A[l], A[r] = A[r], A[l]

    def downheap(self, A, k):
        l = self.left(k)
        r = self.right(k)
        if l < len(A) and self.comparator_function(A[l], A[k]):
            smallest = l
        else:
            smallest = k
        if r < len(A) and self.comparator_function(A[r], A[smallest]):
            smallest = r
        if smallest != k:
            self.swap(A, k, smallest)
            self.downheap(A, smallest)
        else:
            return

    def upheap(self, A, k):
        parent = self.parent(k)
        if parent >= 0 and self.comparator_function(A[k], A[parent]):
            self.swap(A, parent, k)
            self.upheap(A, parent)

    def build_min_heap(self, A):
        n = len(A) // 2 - 1
        for i in range(n, -1, -1):
            self.downheap(A, i)
        return A

    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''

        # Write your code here
        self.data.append(value)
        self.upheap(self.data, len(self.data) - 1)
        pass

    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''

        # Write your code here
        self.swap(self.data, 0, len(self.data) - 1)
        ans = self.data.pop()
        self.downheap(self.data, 0)
        return ans

    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        # Write your code here
        if len(self.data) > 0:
            return self.data[0]
        pass

    # You can add more functions if you want to
