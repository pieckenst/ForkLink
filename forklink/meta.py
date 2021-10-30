import inspect
import sys
import traceback

from .events import *
from .node import Node


class forklinkMixin:
    """forklink Mixin class.

    .. warning::
        You must use this class in conjuction with a discord.py `commands.Cog`.

    Example
    ---------
    .. code:: py

        # forklinkMixin must be used alongside a discord.py cog.
        class MusicCog(commands.Cog, forklink.forklinkMixin):

            @forklink.forklink.listener()
            async def on_node_ready(self, node: forklink.Node):
                 print(f'Node {node.identifier} is ready!')


        def setup(bot: commands.Bot):
            bot.add_cog(MusicCog())
    """

    def __new__(cls, *args, **kwargs):
        listeners = {}

        for name, element in inspect.getmembers(cls):
            try:
                element_listeners = getattr(element, '__forklink_listeners__')
            except AttributeError:
                continue

            for listener in element_listeners:
                try:
                    listeners[listener].append(element.__name__)
                except KeyError:
                    listeners[listener] = [element.__name__]

        self = super().__new__(cls)
        cls.__forklink_listeners__ = listeners

        return self

    async def on_forklink_error(self, listener,  error: Exception):
        """Event dispatched when an error is raised during mixin listener dispatch.

        Parameters
        ------------
        listener:
            The listener where an exception was raised.
        error: Exception
            The excpetion raised when dispatching a mixin listener.
        """
        print(f'Ignoring exception in listener {listener}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def on_node_ready(self, node: Node):
        """Listener dispatched when a :class:`forklink.node.Node` is connected and ready.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        """

    async def on_track_start(self, node: Node, payload: TrackStart):
        """Listener dispatched when a track starts.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        payload: TrackStart
            The :class:`forklink.events.TrackStart` payload.
        """

    async def on_track_end(self, node: Node, payload: TrackEnd):
        """Listener dispatched when a track ends.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        payload: TrackEnd
            The :class:`forklink.events.TrackEnd` payload.
        """

    async def on_track_stuck(self, node: Node, payload: TrackStuck):
        """Listener dispatched when a track is stuck.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        payload: TrackStuck
            The :class:`forklink.events.TrackStuck` payload.
        """

    async def on_track_exception(self, node: Node, payload: TrackException):
        """Listener dispatched when a track errors.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        payload: TrackException
            The :class:`forklink.events.TrackException` payload.
        """

    async def on_websocket_closed(self, node: Node, payload: WebsocketClosed):
        """Listener dispatched when a node websocket is closed by lavalink.

        Parameters
        ------------
        node: Node
            The node associated with the listener event.
        payload: WebsocketClosed
            The :class:`forklink.events.WebsocketClosed` payload.
        """

    @staticmethod
    def listener(event: str = None):
        """Decorator that adds a coroutine as a forklink event listener.

        .. note::
            This must be used within a :class:`forklink.forklinkMixin` subclass in order to work.

        Parameters
        ------------
        event: Optional[str]
            The event name to listen to. E.g "on_node_ready". Defaults to the function name.

        Example
        ---------
        .. code:: py

                @forklink.forklinkMixin.listener(event="on_node_ready")
                async def node_ready_event(node):
                    print(f'Node {node.indentifier} ready!')

        Raises
        --------
        TypeError
            Listener is not a coroutine.
        """
        def wrapper(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('forklink listeners must be coroutines.')

            name = event or func.__name__

            try:
                func.__forklink_listeners__.append(name)
            except AttributeError:
                func.__forklink_listeners__ = [name]

            return func
        return wrapper
