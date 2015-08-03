try:
        import sys
        import inspect
        from Queue import Queue
        from threading import Thread
except ImportError, err:
        from lib.core.core import Core
        Core.print_error(err)


class Worker(Thread):

    def __init__(self, tasks):

        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()


    def run(self):
        """
                Thread basladiginda calisacak kod. self.start() dendiginde calisacak kod parcai
        """

        while True:
                func, args, kargs = self.tasks.get(True, None)

                if not func:
                        break

                try:
                        func(*args, **kargs)
                except Exception, err:
                        pass

                self.tasks.task_done()



class ThreadPool:

    def __init__(self, num_threads):

        self.threads = []

        self.num_threads = num_threads
        self.tasks = Queue(self.num_threads)

        for _ in range(self.num_threads): 
                worker = Worker(self.tasks)
                self.threads.append(worker)


    def add_task(self, func, *args, **kargs):

        self.tasks.put((func, args, kargs))



    def wait_completion(self):

        self.tasks.join()

        for _ in range(self.num_threads):
                self.add_task(None, None, None)

        for t in self.threads:
                t.join()

