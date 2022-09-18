"""
This type stub file was generated by pyright.
"""

import abc
from dataclasses import dataclass
from typing import List, Optional
from pop.configs.network_architecture import NetworkArchitecture
from pop.configs.type_aliases import EventuallyNestedDict

@dataclass(frozen=True)
class ExplorationParameters(abc.ABC):
    def __init__(self, d: dict) -> None:
        ...
    
    @staticmethod
    @abc.abstractmethod
    def network_architecture_fields() -> List[List[str]]:
        ...
    
    @staticmethod
    @abc.abstractmethod
    def get_method() -> str:
        ...
    


@dataclass(frozen=True)
class InverseModelArchitecture:
    embedding: NetworkArchitecture
    action_prediction_stream: NetworkArchitecture
    learning_rate: int
    ...


@dataclass(frozen=True)
class RandomNetworkDistillerArchitecture:
    network: NetworkArchitecture
    learning_rate: int
    ...


@dataclass(frozen=True)
class EpisodicMemoryParameters(ExplorationParameters):
    method: str
    size: int
    neighbors: int
    exploration_bonus_limit: int
    random_network_distiller: RandomNetworkDistillerArchitecture
    inverse_model: InverseModelArchitecture
    @staticmethod
    def get_method() -> str:
        ...
    
    @staticmethod
    def network_architecture_fields() -> List[List[str]]:
        ...
    
    def __init__(self, d: dict) -> None:
        ...
    


@dataclass(frozen=True)
class EpsilonGreedyParameters(ExplorationParameters):
    method: str
    max_epsilon: float
    min_epsilon: float
    epsilon_decay: float
    @staticmethod
    def get_method() -> str:
        ...
    
    def __init__(self, d: dict) -> None:
        ...
    
    @staticmethod
    def network_architecture_fields() -> List[List[str]]:
        ...
    


@dataclass(frozen=True)
class ReplayMemoryParameters:
    alpha: float
    max_beta: float
    min_beta: float
    beta_decay: int
    capacity: int
    ...


@dataclass(frozen=True)
class AgentArchitecture:
    embedding: NetworkArchitecture
    advantage_stream: NetworkArchitecture
    value_stream: NetworkArchitecture
    exploration: ExplorationParameters
    replay_memory: ReplayMemoryParameters
    learning_rate: float
    learning_frequency: int
    target_network_weight_replace_steps: int
    gamma: float
    huber_loss_delta: float
    batch_size: int
    def __init__(self, agent_dict: EventuallyNestedDict = ..., network_architecture_implementation_folder_path: Optional[str] = ..., network_architecture_frame_folder_path: Optional[str] = ..., load_from_dict: dict = ...) -> None:
        ...
    


