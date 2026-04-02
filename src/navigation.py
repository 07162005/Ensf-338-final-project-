from models import Route, NavigationSession


class NavigationManager:
    def __init__(self, graph):
        self.graph = graph

    def navigate(self, session: NavigationSession, source_id: str, destination_id: str):
        # TODO:
        # 1. Call self.graph.shortest_path(...)
        # 2. Push route into session.history
        # 3. Respect session.undo_limit
        # 4. Update session.current_location
        pass

    def undo_last_navigation(self, session: NavigationSession):
        # TODO:
        # Treat session.history as a stack
        # Remove latest route
        # Update current_location to previous route destination
        # or revert to original source when history becomes empty
        pass