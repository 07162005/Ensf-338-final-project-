from models import Route, NavigationSession


class NavigationManager:
    def __init__(self, graph):
        self.graph = graph

    def navigate(self, session: NavigationSession, source_id: str, destination_id: str):
        """
        Perform a navigation from source to destination.
        Updates the session history and current location.
        
        Args:
            session: NavigationSession object
            source_id: Starting building ID
            destination_id: Target building ID
            
        Returns:
            Route object containing the path and total weight
        """
        if not session:
            raise ValueError("Navigation session cannot be None")
        if not source_id or not destination_id:
            raise ValueError("Source and destination must be specified")
        
        try:
            route = self.graph.shortest_path(source_id, destination_id)
        except ValueError as e:
            print(f"Navigation error: {e}")
            raise
        
        navigation_record = {
            'source': source_id,
            'destination': destination_id,
            'route': route,
            'timestamp': self._get_timestamp()
        }
        
        session.history.append(navigation_record)
        
        if len(session.history) > session.undo_limit:
            session.history.pop(0)
        
        session.current_location = destination_id
        
        return route

    def undo_last_navigation(self, session: NavigationSession):
        """
        Undo the last navigation operation.
        Returns True if undo was successful, False otherwise.
        """
        if not session:
            raise ValueError("Navigation session cannot be None")
        
        if not session.history:
            print("No navigation history to undo")
            return False
        
        last_navigation = session.history.pop()
        
        if session.history:
            previous_nav = session.history[-1]
            session.current_location = previous_nav['destination']
        else:
            session.current_location = None
        
        print(f"Undid navigation from {last_navigation['source']} to {last_navigation['destination']}")
        return True
    
    def get_navigation_history(self, session: NavigationSession):
        """Return the complete navigation history for a session."""
        if not session:
            return []
        return session.history.copy()