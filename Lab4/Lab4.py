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
        item = [value, priority]
        self.map[pos] = item
        heapq.heappush(self.max_heap, (-priority, pos))
        heapq.heappush(self.min_heap, (priority, pos))
        self.order.append(pos)