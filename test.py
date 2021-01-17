import time
from mthread.base import BaseWorker

class WorkerThread(BaseWorker):
    def __init__(self):
        super().__init__()

    def processRequest(self, reqObj):
        print(reqObj)

print('Initilizing a Worker instance ...')
worker = WorkerThread()

print('Starting the worker ...')
worker.start()

for i in range(3):
    print('Loop {}'.format(i))
    localTime = time.strftime("%H:%M:%S", time.localtime())
    worker.request(localTime)

print('Sending termination request to the worker ...')
worker.stop()
