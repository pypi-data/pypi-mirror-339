
import concurrent.futures
import atexit

class ThreadPool:
  def __init__(self, thread_num):
    self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=thread_num)
    atexit.register(lambda: self.executor.shutdown())

  def batch(self, tasks):
    tasks1 = list(tasks)
    futures = [self.executor.submit(task) for task in tasks1]
    results = []
    i = len(tasks1)
    while i > 0:
      index = i - 1
      if futures[index].cancel():
        result = tasks1[index]()
        results.append(result)
        i = index
      else:
        break

    results0 = [future.result() for future in futures[0:i]]
    results.reverse()
    return results0 + results
