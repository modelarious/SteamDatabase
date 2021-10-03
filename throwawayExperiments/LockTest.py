from multiprocessing import Pool, Lock
from time import sleep

def do_job(i):
    "The greater i is, the shorter the function waits before returning."
    with lock:
        print("I have the lock")
        sleep(1-(i/10.))
        print("I let go of the lock")
        return i

def init_child(lock_):
    global lock
    lock = lock_

def main():
    lock = Lock()
    poolsize = 4
    with Pool(poolsize, initializer=init_child, initargs=(lock,)) as pool:
        results = pool.imap_unordered(do_job, range(poolsize))
        print(list(results))

if __name__ == "__main__":
    main()