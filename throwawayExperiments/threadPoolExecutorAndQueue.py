# from concurrent.futures import ThreadPoolExecutor
# END_OF_QUEUE = None

# from collections import deque
from multiprocessing import Manager
# m = Manager()
# # gameNameMatchesProcessingQueue = m.Queue()
# # userInputRequiredQueue = m.Queue()
# queue = m.Queue()


# myList = []
# for i in range(20):
#     myList.append("hello")

# queue.queue = deque(myList)
# queue.put(END_OF_QUEUE)

# def run(strVal):
#     print(strVal)


# with ThreadPoolExecutor() as executor:
#     executor.map(run, iter(queue.get, END_OF_QUEUE))


import queue

l = [i for i in range(1000)]

m = Manager()
q2 = m.Queue()
q2.queue = queue.deque(l)

for i in range(1000):
    print(q2.get())