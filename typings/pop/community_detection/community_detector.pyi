"""
This type stub file was generated by pyright.
"""

import networkx as nx
from typing import FrozenSet, List, Optional, Set, Tuple

Community = FrozenSet[int]
class CommunityDetector:
    def __init__(self, seed: int, resolution: float = ..., threshold: float = ..., enable_power_supply_modularity=...) -> None:
        ...
    
    @staticmethod
    def community_coherence(graph: nx.Graph, community: Set[int]) -> int:
        ...
    
    @staticmethod
    def community_degree(graph: nx.Graph, community: Set[int]) -> int:
        ...
    
    @staticmethod
    def get_community(node: int, communities: List[Set[int]]) -> Set[int]:
        ...
    
    def initialize_intermediate_community_structure(self, graph_t: nx.Graph, graph_t1: nx.Graph, comm_t: List[Set[int]]) -> Tuple[Set[Set[int]], Set[Tuple[int, int]]]:
        """
        Takes C_t, community structure at time t, and modifies it by selecting singletons and two-vertices
        communities.
        Node structure does not change in our case thus we skip it, we only consider edge addition/deletion
        :param graph_t: graph at previous timestep
        :param graph_t1: current graph
        :param comm_t: community structure at previous timestep
        :return
        - C_1: a set of communities to be separated into singleton communities
        - C_2: a set of two-vertices communities to be created
        """
        ...
    
    def dynamo(self, graph_t: nx.Graph, graph_t1: Optional[nx.Graph] = ..., comm_t: Optional[List[Set[int]]] = ..., alpha: float = ..., beta: float = ...) -> List[FrozenSet[int]]:
        """
        Two phases:
        - initialize an intermediate community structure
        - repeat the last two steps of Louvain algorithm on the intermediate
          community structure until the modularity gain is negligible
        """
        ...
    


