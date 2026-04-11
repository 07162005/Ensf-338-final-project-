from models import ServiceRequest, IncomingRequest


class RequestQueue:
    def __init__(self):
        self.queue = []   # FIFO queue

    def enqueue(self, request: IncomingRequest):
        self.queue.append(request)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0


class PriorityServiceQueue:
    def __init__(self):
        self.requests = []   # list of ServiceRequest objects

    def add_request(self, request: ServiceRequest):
        # Add request
        self.requests.append(request)

        # Sort by:
        # 1. Higher priority first (-priority)
        # 2. Earlier timestamp first
        self.requests.sort(key=lambda r: (-r.priority, r.timestamp))

    def serve_next(self):
        if self.is_empty():
            print("No service requests available")
            return None

        return self.requests.pop(0)

    def is_empty(self):
        return len(self.requests) == 0