import unittest
from litepolis_database_example import (
    DEFAULT_CONFIG,
    DatabaseActor
)

class TestExports(unittest.TestCase):
    def test_default_config_exists(self):
        self.assertIsNotNone(DEFAULT_CONFIG, "DEFAULT_CONFIG should be exported")

    def test_database_actor_exists(self):
        self.assertIsNotNone(DatabaseActor, "DatabaseActor should be exported")
