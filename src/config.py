import threading
import tomllib
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT = get_project_root()

class MCPServerConfig(BaseModel):
    """Configuration for a single MCP server"""

    command: Optional[str] = Field(None, description="Command for stdio connections")
    env: Dict[str,str] = Field(
        default_factory=dict, description="env for stdio command"
    )

class AgentSettings(BaseModel):
    model: str = Field(..., description="Model name")
    base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key")
    mcp: Optional[list[MCPServerConfig]] = Field(
        default_factory=list, description="Arguments for stdio command"
    )


class AppConfig(BaseModel):
    agents: Dict[str, AgentSettings]


class Config:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config = None
                    self._load_initial_config()
                    self._initialized = True

    @staticmethod
    def _get_config_path() -> Path:
        root = PROJECT_ROOT
        config_path = root / "config" / "config.toml"
        if config_path.exists():
            return config_path
        raise FileNotFoundError("No configuration file found in config directory")

    def _load_config(self) -> dict:
        config_path = self._get_config_path()
        with config_path.open("rb") as f:
            return tomllib.load(f)

    def _load_initial_config(self):
        raw_config = self._load_config()

        repo_agent = raw_config.get("repo_agent", {})
        repo_settings = AgentSettings(
            model=repo_agent.get("model"),
            base_url=repo_agent.get("base_url"),
            api_key=repo_agent.get("api_key"),
        )

        community_agent = raw_config.get("community_agent", {})
        community_settings = AgentSettings(
            model=community_agent.get("model"),
            base_url=community_agent.get("base_url"),
            api_key=community_agent.get("api_key"),
            mcp=[MCPServerConfig(
                command=community_agent.get("GITHUB_MCP_SERVER_COMMAND"),
                env={"GITHUB_PERSONAL_ACCESS_TOKEN":community_agent.get("GITHUB_PERSONAL_ACCESS_TOKEN")}
            )]
        )

        manager_agent = raw_config.get("manager_agent", {})
        manager_settings = AgentSettings(
            model=manager_agent.get("model"),
            base_url=manager_agent.get("base_url"),
            api_key=manager_agent.get("api_key"),
        )

        self._config = AppConfig(
            agents={
                "repo_agent": repo_settings,
                "community_agent": community_settings,
                "manager_agent": manager_settings,
            }
        )

    @property
    def repo_agent(self) -> AgentSettings:
        return self._config.agents["repo_agent"]

    @property
    def community_agent(self) -> AgentSettings:
        return self._config.agents["community_agent"]

    @property
    def manager_agent(self) -> AgentSettings:
        return self._config.agents["manager_agent"]

    @property
    def root_path(self) -> Path:
        """Get the root path of the application"""
        return PROJECT_ROOT


config = Config()

