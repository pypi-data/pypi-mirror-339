import json
import os
from typing import Dict, Optional, Any, Union

class SecretsManager:
    """
    Manager for storing and retrieving secrets.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize a secrets manager.
        
        Args:
            config_file: Optional path to a JSON config file
        """
        self._secrets: Dict[str, Any] = {}
        
        if config_file:
            self.load_from_file(config_file)
        
        elif os.path.exists("manaflow.json"):
            self.load_from_file("manaflow.json")
    
    def set_secret(self, key: str, value: Union[str, Dict[str, Any]]) -> None:
        """
        Set a secret value.
        
        Args:
            key: The secret key
            value: The secret value, can be a string or a dictionary of values
        """
        self._secrets[key] = value
    
    def get_secret(self, key: str) -> Optional[Any]:
        """
        Get a secret value.
        
        Args:
            key: The secret key
            
        Returns:
            The secret value, or None if not found
        """
        return self._secrets.get(key)
    
    def delete_secret(self, key: str) -> None:
        """
        Delete a secret.
        
        Args:
            key: The secret key
        """
        if key in self._secrets:
            del self._secrets[key]
    
    def clear(self) -> None:
        """Clear all secrets."""
        self._secrets.clear()
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load secrets from a JSON file.
        
        Args:
            file_path: Path to the JSON file
        """
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
                for key, value in config.items():
                    self.set_secret(key, value)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading secrets from {file_path}: {e}")
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save secrets to a JSON file.
        
        Args:
            file_path: Path to the JSON file
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self._secrets, f, indent=2)
        except Exception as e:
            print(f"Error saving secrets to {file_path}: {e}")


secrets_manager = SecretsManager()
