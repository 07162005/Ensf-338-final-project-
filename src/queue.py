class RequestQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, request):
        self.queue.append(request)

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

    def peek(self):
        if len(self.queue) == 0:
            return None
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


class PriorityServiceQueue:
    def __init__(self):
        self.requests = []

    def add_request(self, request):
        self.requests.append(request)
        self.requests.sort(key=lambda r: (-r.priority, r.timestamp))

    def serve_next(self):
        if len(self.requests) == 0:
            return None
        return self.requests.pop(0)

    def peek(self):
        if len(self.requests) == 0:
            return None
        return self.requests[0]

    def is_empty(self):
        return len(self.requests) == 0

    def size(self):
        return len(self.requests)
