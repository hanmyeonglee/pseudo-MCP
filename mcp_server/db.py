import threading, time

IDS = set()
DB = dict()

__lock = threading.Lock()

def __clean():
    while True:
        with __lock:
            current = time.time()
            delete = set(id for id, T in DB.items() if (T - current) >= 3600)
            IDS -= delete
            for id in delete: del DB[id]

        time.sleep(60)

cleaner = threading.Thread(target=__clean, daemon=True)
cleaner.start()