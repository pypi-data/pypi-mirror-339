import json
from pathlib import Path
from typing import Any, Dict, Optional
from ..exceptions import FileOperationError, ConfigurationError

class BaseService:
    """Base service class with common functionality."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the service with optional config directory."""
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".lightwave"
        self.ensure_config_dir()
    
    def ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ConfigurationError(f"Failed to create config directory: {e}")
    
    def read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Read and parse a JSON file."""
        try:
            if not file_path.exists():
                return {}
            with file_path.open('r') as f:
                return json.load(f)
        except Exception as e:
            raise FileOperationError(f"Failed to read JSON file {file_path}: {e}")
    
    def write_json_file(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Write data to a JSON file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            raise FileOperationError(f"Failed to write JSON file {file_path}: {e}")
    
    def get_data_file_path(self, filename: str) -> Path:
        """Get the full path for a data file."""
        return self.config_dir / filename 