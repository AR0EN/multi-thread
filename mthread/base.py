import threading
import queue
import time
from abc import ABC, abstractmethod

class BaseWorker(ABC):
    insCountLock = threading.Lock()
    __insCount = 0

    def __init__(self):
        self.id = BaseWorker.getInsCount()
        BaseWorker.incInsCount()

        self.__mThread = threading.Thread(target=self.run)
        self.__eTermination = threading.Event()
        self.__reqQueueLock = threading.Lock()
        self.__reqQueue = queue.Queue()

    def start(self):
        if (not self.__mThread.is_alive()):
            self.__mThread.start()
            return True
        else:
            print('Thread has been started!')
            return False

    def stop(self):
        if (self.__mThread.is_alive()):
            self.__eTermination.set()
            self.__mThread.join()
        else:
            return False

    def request(self, reqObj):
        if (self.__eTermination.isSet()):
            print('Thread has been terminated!')
            result = False
        elif (reqObj is None):
            print('Invalid Request Object!')
            result = False
        else:
            try:
                self.__reqQueue.put(reqObj)
                result = True
            except Queue.Full as e:
                result = False
                print('Thread is busy!')
            except Exception as e:
                result = False
                print('Could not add request to the queue, Unknown Error!')
                print(e)

        return result

    def run(self):
        while(not self.__eTermination.isSet()):
            try:
                if (not self.__reqQueue.empty()):
                    self.processRequest(self.__reqQueue.get(timeout=1))
            except Queue.Empty as e:
                print(e)

        print('Received termination request, cleaning-up request queue ...')

        while (not self.__reqQueue.empty()):
            try:
                self.processRequest(self.__reqQueue.get(timeout=1))
            except Queue.Empty as e:
                pass
            except Exception as e:
                print(e)

        print('Terminating ...')

    @abstractmethod
    def processRequest(self, reqObj):
        pass

    @staticmethod
    def getInsCount():
        with BaseWorker.insCountLock:
            count = BaseWorker.__insCount
        return count

    @staticmethod
    def incInsCount():
        with BaseWorker.insCountLock:
            BaseWorker.__insCount += 1
            count = BaseWorker.__insCount
        return count