from abc import abstractmethod

import torch as th
import torch.nn as nn
import dgl
from dgl.heterograph import DGLHeteroGraph
from torch import Tensor, FloatTensor

from GNN.gcn import GCN


class DuelingGCN(GCN):
    def __init__(
        self,
        node_features: int,
        edge_features: int,
        action_space_size: int,
        architecture_path: str,
        name: str,
        log_dir: str = "./",
    ):
        super(DuelingGCN, self).__init__(
            node_features, edge_features, architecture_path, name, log_dir
        )

        # Parameters
        self.node_features = node_features
        self.edge_features = edge_features
        self.action_space_size = action_space_size

        # Network Paths
        self.advantage_stream: nn.Module = self.init_advantage_stream(action_space_size)
        self.value_stream: nn.Module = self.init_value_stream()

    def init_advantage_stream(self, action_space_size: int) -> nn.Module:
        return nn.Sequential(
            nn.Linear(
                self.architecture["hidden_output_size"]
                * self.architecture["heads"][-1],
                self.architecture["advantage_stream_size"],
            ),
            nn.ReLU(),
            nn.Linear(self.architecture["advantage_stream_size"], action_space_size),
        )

    def init_value_stream(self) -> nn.Module:
        return nn.Sequential(
            nn.Linear(
                self.architecture["hidden_output_size"]
                * self.architecture["heads"][-1],
                self.architecture["value_stream_size"],
            ),
            nn.ReLU(),
            nn.Linear(self.architecture["value_stream_size"], 1),
        )

    @abstractmethod
    def extract_features(self, g: DGLHeteroGraph) -> Tensor:
        """
        Embed graph by graph convolutions

        Parameters
        ----------
        g: :class:`DGLHeteroGraph`
            input graph with node and edge features

        Return
        ------
        graph_embedding: :class:`Tensor`
            graph embedding computed from node embeddings
        """
        ...

    @staticmethod
    def compute_graph_embedding(
        g: DGLHeteroGraph, node_embeddings: th.Tensor
    ) -> th.Tensor:

        g.ndata["node_embeddings"] = node_embeddings
        graph_embedding: Tensor = dgl.mean_nodes(g, "node_embeddings")
        del g.ndata["node_embeddings"]
        return graph_embedding

    def forward(self, g: DGLHeteroGraph) -> Tensor:
        graph_embedding: Tensor = self.extract_features(g)

        # Compute value of current state
        state_value: float = self.value_stream(graph_embedding)

        # Compute advantage of (current_state, action) for each action
        state_advantages: FloatTensor = self.advantage_stream(graph_embedding)

        q_values: Tensor = state_value + (state_advantages - state_advantages.mean())
        return q_values

    def advantage(self, g: DGLHeteroGraph) -> Tensor:
        """
        Advantage value for each state-action pair

        Parameters
        ----------
        g: :class:`DGLHeteroGraph`
            input graph

        Return
        ------
        state_advantages: :class: `Tensor`
            state-action advantages

        """

        graph_embedding: Tensor = self.extract_features(g)

        # Compute advantage of (current_state, action) for each action
        state_advantages: FloatTensor = self.advantage_stream(graph_embedding)

        return state_advantages

    def save(self):
        """
        Save a checkpoint of the network.
        Save all the hyperparameters.
        """
        checkpoint = {
            "name": self.name,
            "network_state": self.state_dict(),
            "node_features": self.node_features,
            "edge_features": self.edge_features,
            "action_space_size": self.action_space_size,
        }
        checkpoint = checkpoint | self.architecture
        th.save(checkpoint, self.log_file)

    def load(
        self,
        log_dir: str,
    ):
        checkpoint = th.load(log_dir)
        self.name = checkpoint["name"]
        self.load_state_dict(checkpoint["network_state"])
        self.node_features = checkpoint["node_features"]
        self.edge_features = checkpoint["edge_features"]
        self.action_space_size = checkpoint["action_space_size"]
        self.architecture = {
            i: j
            for i, j in checkpoint.items()
            if i
            not in {
                "network_state",
                "node_features",
                "edge_features",
                "action_space_size",
                "name",
            }
        }
        print("Network Succesfully Loaded!")
