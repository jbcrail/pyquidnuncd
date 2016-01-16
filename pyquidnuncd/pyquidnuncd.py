import Queue
import socket
import threading
import time


class Client(object):
    EOL = '\r\n'

    def __init__(self, hostname='localhost', port=3230):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((hostname, port))
        self._fd = self._socket.makefile()

    def do(self, cmd='INFO'):
        d = {}
        self._fd.write(cmd + self.EOL)
        self._fd.flush()
        while True:
            line = self._fd.readline().rstrip()
            if line == '':
                break
            fields = line.split('=')
            if len(fields) == 1:
                d[fields[0]] = fields[0]
            else:
                d[fields[0]] = fields[1]
        return d

    def close(self):
        self._fd.close()
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()


def stream(client, cmd='INFO', interval=1.0, shutdown=None):
    try:
        while True:
            if shutdown and shutdown.is_set():
                break
            result = client.do(cmd)
            if shutdown:
                shutdown.wait(timeout=interval)
            else:
                time.sleep(interval)
            yield result
    except Exception as e:
        pass
    else:
        client.close()


def enqueue(stream, queue):
    try:
        for item in stream:
            queue.put(item)
    except Exception as e:
        pass
    finally:
        queue.put(StopIteration)


def dequeue(queue):
    while True:
        item = queue.get()
        if item is StopIteration:
            break
        yield item


def join(streams):
    for s in streams:
        for item in s:
            yield item


def multiplex(streams):
    q = Queue.Queue()
    consumers = []
    for s in streams:
        thr = threading.Thread(target=enqueue, args=(s, q))
        thr.start()
        consumers.append(dequeue(q))
    return join(consumers)
