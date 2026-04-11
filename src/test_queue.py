from queue import RequestQueue, PriorityServiceQueue
from models import ServiceRequest, IncomingRequest


def run_queue_tests():
    print("=== FIFO Queue Test ===")
    rq = RequestQueue()

    rq.enqueue(IncomingRequest("Q1", "navigation", None, 1))
    rq.enqueue(IncomingRequest("Q2", "service", None, 2))
    rq.enqueue(IncomingRequest("Q3", "navigation", None, 3))

    while not rq.is_empty():
        req = rq.dequeue()
        print("Processed:", req.request_id)

    print("\n=== Priority Queue Test ===")
    pq = PriorityServiceQueue()

    r1 = ServiceRequest("R1", "Alice", "IT", "Projector broken", 2, 1)
    r2 = ServiceRequest("R2", "Bob", "Maintenance", "Water leak", 3, 2)
    r3 = ServiceRequest("R3", "Charlie", "Help Desk", "Login reset", 1, 3)
    r4 = ServiceRequest("R4", "Diana", "IT", "Lab PCs down", 3, 4)

    pq.add_request(r1)
    pq.add_request(r2)
    pq.add_request(r3)
    pq.add_request(r4)

    while not pq.is_empty():
        req = pq.serve_next()
        print("Served:", req.request_id, "| Priority:", req.priority)


if __name__ == "__main__":
    run_queue_tests()