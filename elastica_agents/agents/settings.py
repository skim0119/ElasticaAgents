import os
from mcp_agent.config import Settings


def get_settings(model: str, workdir: str) -> Settings:
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
                "path_pattern": workdir + "/logs/mcp-agent-{unique_id}.jsonl",
                "unique_id": "timestamp",  # Options: "timestamp" or "session_id"
                # "timestamp_format": "%Y%m%d_%H%M%S",
            },
        },
        "mcp": {
            "servers": {
                "fetch": {
                    "command": "uvx",
                    "args": ["mcp-server-fetch"],
                },
                "filesystem": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        workdir,
                    ],
                },
            }
        },
        "openai": {
            "default_model": model,
            "api_key": os.environ.get("OPENAI_API_KEY"),
        },
    }

    default_setting = Settings(
        **default_setting_dict,
    )
    default_setting.otel.console_debug = True
    default_setting.usage_telemetry.enable_detailed_telemetry = True

    return default_setting
