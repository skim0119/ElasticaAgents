import os
from mcp_agent.config import Settings


def get_settings(model: str | None = None, workdir: str | None = None) -> Settings:
    """
    Factory function to create settings for the ElasticaAgents
    """
    default_setting_dict = {
        "execution_engine": "asyncio",
        "logger": {
            "transports": ["console", "file"],
            "level": "debug",
            "progress_display": True,
            "path_settings": {
                "path_pattern": "logs/mcp-agent-{unique_id}.jsonl",
                "unique_id": "timestamp",  # Options: "timestamp" or "session_id"
                "timestamp_format": "%Y%m%d_%H%M%S",
            },
        },
        "mcp": {
            "servers": {
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        workdir,
                    ],
                }
            }
        },
        "openai": {
            "default_model": model or "gpt-4o-mini",
            "api_key": os.environ.get("OPENAI_API_KEY"),
        },
    }

    default_setting = Settings(
        **default_setting_dict,
    )
    return default_setting
