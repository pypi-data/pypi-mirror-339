import asyncio
from typing import Any, Callable, Dict, List, Union
import logging
from .models.inbound import BaseMessage
from .exceptions import InvalidMessageTypeError

logger = logging.getLogger(__name__)

class EventDispatcher:
    """Dispatches events to registered handlers."""
    
    def __init__(self):
        """Initialize the event dispatcher."""
        self._handlers: Dict[str, List[Callable[[BaseMessage], Any]]] = {}
    
    def register(self, event_type: str, handler: Callable[[BaseMessage], Any]) -> None:
        """Register a handler for an event type.
        
        Args:
            event_type: The event type to register the handler for
            handler: The handler function to register
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append(handler)
        logger.debug(f"Registered handler for event type {event_type}")
    
    # Alias for backward compatibility
    register_handler = register
    
    async def dispatch(self, event_type: str, data: Any) -> None:
        """Dispatch an event to all registered handlers.
        
        Args:
            event_type: The event type to dispatch
            data: The message data to pass to the handlers
        """
        # We need to check if data is a subclass of BaseMessage, not strictly BaseMessage
        from .models.inbound import BaseMessage
        if not isinstance(data, BaseMessage):
            logger.error(f"Cannot dispatch event: expected a subclass of BaseMessage, got {type(data).__name__}")
            return
            
        handlers = self._handlers.get(event_type, [])
        if not handlers:
            logger.debug(f"No handlers registered for event type {event_type}")
            return
            
        logger.debug(f"Dispatching event {event_type} to {len(handlers)} handlers")
        
        for handler in handlers:
            try:
                result = handler(data)
                if asyncio.iscoroutine(result):
                    try:
                        await result
                    except Exception as e:
                        logger.error(f"Error in async handler for event {event_type}: {e}")
                        logger.error(traceback.format_exc())
            
            except Exception as e:
                logger.error(f"Error in handler for event {event_type}: {e}")
                import traceback
                logger.error(traceback.format_exc())
