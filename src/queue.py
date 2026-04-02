from models import ServiceRequest, IncomingRequest


class RequestQueue:
    def __init__(self):
        self.queue = []   # use as FIFO queue

    def enqueue(self, request: IncomingRequest):
        # TODO:
        # Add request to end of queue
        pass

    def dequeue(self):
        # TODO:
        # Remove and return first request in queue
        # Since you're allowed to use lists, you can use pop(0)
        # or later improve with front index if you want
        pass

    def is_empty(self):
        return len(self.queue) == 0


class PriorityServiceQueue:
    def __init__(self):
        self.requests = []   # list of ServiceRequest objects
                             # You should implement priority behavior yourself

    def add_request(self, request: ServiceRequest):
        # TODO:
        # Add request and maintain correct priority order
        #
        # Option 1:
        # Insert into correct position manually
        #
        # Option 2:
        # Append first, then reorder based on priority and timestamp
        pass

    def serve_next(self):
        # TODO:
        # Remove and return highest-priority request
        pass

    def is_empty(self):
        return len(self.requests) == 0