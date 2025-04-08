import unittest
from manaflow.secrets import secrets_manager


class TestSecretsManager(unittest.TestCase):
    def setUp(self):
        secrets_manager.clear()
        
    def test_set_get_secret(self):
        secrets_manager.set_secret("test_key", "test_value")
        self.assertEqual(secrets_manager.get_secret("test_key"), "test_value")
        
    def test_get_nonexistent_secret(self):
        self.assertIsNone(secrets_manager.get_secret("nonexistent_key"))
        
    def test_delete_secret(self):
        secrets_manager.set_secret("test_key", "test_value")
        secrets_manager.delete_secret("test_key")
        self.assertIsNone(secrets_manager.get_secret("test_key"))
        
    def test_clear_secrets(self):
        secrets_manager.set_secret("test_key1", "test_value1")
        secrets_manager.set_secret("test_key2", "test_value2")
        secrets_manager.clear()
        self.assertIsNone(secrets_manager.get_secret("test_key1"))
        self.assertIsNone(secrets_manager.get_secret("test_key2"))


if __name__ == "__main__":
    unittest.main()
