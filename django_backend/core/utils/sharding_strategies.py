from abc import ABC, abstractmethod


class AbstractShardingStrategy(ABC):
    """
    Abstract sharding strategy.
    """

    @abstractmethod
    def get_shard(self, *args, **kwargs) -> str:
        pass


class ShardingModuloStrategy(AbstractShardingStrategy):
    """
    Sharding strategy that uses modulo to determine shard.
    """

    def __init__(self, shards: list[str]):
        self.shards = shards

    def get_shard(self, uid: int) -> str:
        """
        Get shard for id.
        """
        shard_index = uid % len(self.shards)
        return self.shards[shard_index]


class ShardingBasedOnTopicStrategy(AbstractShardingStrategy):
    """
    Sharding strategy that uses topic to determine shard.
    """

    def __init__(self, shards: dict[int:str]):
        self.shards = shards

    def get_shard(self, topic_id: int) -> str:
        """
        Get shard based on topic.
        """
        return self.shards[topic_id]


def get_sharding_strategy(shards) -> AbstractShardingStrategy:
    """
    Get sharding strategy.
    """
    return ShardingBasedOnTopicStrategy(shards)
