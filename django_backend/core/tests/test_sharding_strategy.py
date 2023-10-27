from django.test import TestCase

from core.utils.sharding_strategies import get_sharding_strategy
from core.utils import (
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
    ARTICLES_DB_SHARDS,
)


articles_sharding_strategy = get_sharding_strategy(shards=ARTICLES_DB_SHARDS)


class ShardingStrategyTestCase(TestCase):
    def test_should_get_shard(self):
        """
        Should get the correct shard.
        """
        shard = articles_sharding_strategy.get_shard(topic_id=1)
        self.assertEqual(shard, ARTICLES_A_DB_ALIAS)

        shard = articles_sharding_strategy.get_shard(topic_id=2)
        self.assertEqual(shard, ARTICLES_B_DB_ALIAS)

        shard = articles_sharding_strategy.get_shard(topic_id=3)
        self.assertEqual(shard, ARTICLES_C_DB_ALIAS)
