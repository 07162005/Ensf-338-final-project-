class NavigationManager:
    def __init__(self, graph):
        self.graph = graph

    def navigate(self, session, source_id: str, destination_id: str):
        route = self.graph.shortest_path(source_id, destination_id)
        if route is None:
            return None

        session.history.append(route)
        if len(session.history) > session.undo_limit:
            session.history.pop(0)
        session.current_location = destination_id
        return route

    def undo_last_navigation(self, session):
        if len(session.history) == 0:
            return None

        last_route = session.history.pop()

        if len(session.history) == 0:
            session.current_location = last_route.source_id
        else:
            session.current_location = session.history[-1].destination_id

        return last_route