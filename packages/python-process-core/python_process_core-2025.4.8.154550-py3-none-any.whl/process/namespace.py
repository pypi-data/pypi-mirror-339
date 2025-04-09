from typing import Self, Optional, ClassVar
from asyncua import Server
from asyncua.common.node import Node
from asyncua.ua.uatypes import NodeId


class NameSpace:
    '''
    '''
    NAMESPACE_ARRAYS: ClassVar[dict[Server, list[str]]] = {}

    def __init__(self, server: Server, idx: int):
        self._server: Server = server
        self._idx: int = idx

    @property
    def server(self) -> Server:
        """
        The server associated with the namespace.
        """
        return self._server
    
    @property
    def idx(self) -> int:
        """
        The index of the namespace.
        """
        return self._idx

    @property
    def uri(self) -> str:
        """
        The URI of the namespace.
        """
        return self.NAMESPACE_ARRAYS[self.server][self.idx]
    
    async def add_object(
        self, 
        name: str, 
        object_type: Optional[NodeId | int] = None,
        instantiate_optional: bool = True,
    ) -> Node:
        """
        Add an object to the namespace.
        """
        return await self.server.nodes.objects.add_object(self.idx, name)
    
    @classmethod
    async def create(cls, server: Server, uri: str) -> Self:
        """
        Create a new namespace in the server with the given URI.
        """
        idx: int = await server.register_namespace(uri=uri)
        cls.NAMESPACE_ARRAYS[server] = await server.get_namespace_array()
        return cls(server=server, idx=idx)
    
    @classmethod
    async def update_namespace_arrays(cls):
        """
        Update the namespace arrays for all servers.
        """
        for server in cls.NAMESPACE_ARRAYS.keys():
            cls.NAMESPACE_ARRAYS[server] = await server.get_namespace_array()