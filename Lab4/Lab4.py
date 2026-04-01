import heapq
from collections import deque

class BiPriorityQueue:
    
    def __init__(self):
        self.max_heap = []
        self.min_heap = []
        self.order = deque()
        self.map = {}
        self.counter = 0
        
    def enqueue(self, value, priority):
        pos = self.counter
        item = [value, priority, False]
        self.map[pos] = item
        heapq.heappush(self.max_heap, (-priority, pos))
        heapq.heappush(self.min_heap, (priority, pos))
        self.order.append(pos)
        
    def _cleanup(self, option):
        if option == "highest":
            while self.max_heap and self.map[self.max_heap[0][1]][2]:
                heapq.heappop(self.max_heap)
        elif option == "lowest":
            while self.min_heap and self.map[self.min_heap[0][1]][2]:
                heapq.heappop(self.min_heap)
        elif option == "oldest":
            while self.order and self.map[self.order[0]][2]:
                self.order.popleft()
        elif option == "newest":
            while self.order and self.map[self.order[-1]][2]:
                self.order.pop()
                
    def peek(self, option):
        self._cleanup(option)
        
        if option == "highest" and self.max_heap:
            return self.map[self.max_heap[0][1]][0]
        elif option == "lowest" and self.min_heap:
            return self.map[self.min_heap[0][1]][0]
        elif option == "oldest" and self.order:
            return self.map[self.order[0]][0]
        elif option == "newest" and self.order:
            return self.map[self.order[-1]][0]
         
    def dequeue(self, option):
        self._cleanup(option)
        
        entry_id = None
        if option == "highest" and self.max_heap:
            _, entry_id = heapq.heappop(self.max_heap)
        elif option == "lowest" and self.min_heap:
            _, entry_id = heapq.heappop(self.min_heap)
        elif option == "oldest" and self.order:
            entry_id = self.order.popleft()
        elif option == "newest" and self.order:
            entry_id = self.order.pop()
        
        if entry_id != None:
            item, priority, _ = self.map[entry_id]
            self.map[entry_id][2] = True
            return 0
        
        raise IndexError("No elements to delete")