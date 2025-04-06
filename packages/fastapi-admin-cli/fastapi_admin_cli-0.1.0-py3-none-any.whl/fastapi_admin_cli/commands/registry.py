import typer
from typing import Dict, Type, List

class CommandRegistry:
    """Registry for managing FastAPI admin commands."""
    
    def __init__(self):
        self._commands: Dict[str, typer.Typer] = {}

    def register(self, name: str, command: typer.Typer):
        """Register a command with the registry."""
        self._commands[name] = command

    def get_command(self, name: str) -> typer.Typer:
        """Get a command by name."""
        return self._commands.get(name)

    def get_all_commands(self) -> Dict[str, typer.Typer]:
        """Get all registered commands."""
        return self._commands

# Global registry instance
registry = CommandRegistry()
