from collections import OrderedDict, defaultdict
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from . import protocols

if TYPE_CHECKING:
    from .Graph import Graph
    from .Node import Node


class Bridge:
    """A Bridge object collects and tracks multiple Graphs in order to facilitate interaction between them.
    The order in which Graphs added matters as Graphs can only get values from previous Graphs/

    Attributes:
        id_to_graph (Dict[int, Graph]): Mapping of graph id to Graph.
        graph_stack (List[Graph]): Stack of visited Intervention Graphs.
        bridged_nodes (defaultdict[Node, List[Node]]): Mapping of bridged Nodes to the BridgeProtocol nodes representing them on different graphs. 
        locks (int): Count of how many entities are depending on ties between graphs not to be released.
    """

    def __init__(self) -> None:

        # Mapping fro Graph if to Graph.
        self.id_to_graph: Dict[int, "Graph"] = OrderedDict()
        # Stack to keep track of most inner current graph
        self.graph_stack: List["Graph"] = list()
        self.bridged_nodes: defaultdict[Node, List[Node]] = defaultdict(lambda: list())

        self.locks = 0

    @property
    def release(self) -> bool:

        return not self.locks

    def add(self, graph: "Graph") -> None:
        """Adds Graph to Bridge.

        Args:
            graph (Graph): Graph to add.
        """

        protocols.BridgeProtocol.set_bridge(graph, self)

        self.id_to_graph[graph.id] = graph

        self.graph_stack.append(graph)

    def peek_graph(self) -> "Graph":
        """Gets the current hierarchical Graph in the Bridge.

        Returns:
            Graph: Graph of current context.

        """
        return self.graph_stack[-1]

    def pop_graph(self) -> None:
        """Pops the last Graph in the graph stack."""

        self.graph_stack.pop()

    def get_graph(self, id: int) -> "Graph":
        """Returns graph from Bridge given the Graph's id.

        Args:
            id (int): Id of Graph to get.

        Returns:
            Graph: Graph.
        """

        return self.id_to_graph[id]
    
    def add_bridge_node(self, node: "Node", bridge_node: "Node") -> None:
        """ Adds a BridgeProtocol to the bridged nodes attribute.

        Args:
            - node (Node): Bridged Node.
            - bridge_node (Node): BridgeProtocol node of the bridged node.
        """ 

        self.bridged_nodes[node].append(bridge_node)

    def get_bridge_node(self, node: "Node", graph_id: int) -> Optional["Node"]:
        """ Check if the argument Node is bridged within the specified graph and returns its corresponding BridgeProtocol node.

        Args:
            - node (Node): Node.
            - graph_id (int): Graph id.

        Returns: 
            Optional[Node]: Bridge Node if it exists.
        """

        for bridge_node in self.bridged_nodes_dict[node]:
            if bridge_node.graph.id == graph_id:
                return bridge_node

        return None
