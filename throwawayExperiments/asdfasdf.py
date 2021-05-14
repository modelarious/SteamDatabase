from multiprocessing import Queue
from queue import deque

gamesOnDisk = ["One", "Two", "Three"]
# gameInputQueue = Queue()
# gameInputQueue.queue = deque(gamesOnDisk)
# print("first value is", gameInputQueue.get())


gameInputQueue = Queue()
for item in gamesOnDisk:
    gameInputQueue.put(item)
print("first value is", gameInputQueue.get())