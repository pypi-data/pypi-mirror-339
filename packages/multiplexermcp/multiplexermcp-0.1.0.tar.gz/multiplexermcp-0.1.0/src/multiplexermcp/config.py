import json
from os import getenv
from easymcp.client.transports.stdio import StdioServerParameters

# this file is a mess

__all__ = [
    "servers_to_run",
]

# load enabled servers from environment variable
enabled_servers_env = getenv("ENABLED_SERVERS")
if enabled_servers_env is None:
    raise Exception("Environment variable ENABLED_SERVERS is not set")

enabled_servers = json.loads(enabled_servers_env)
assert isinstance(enabled_servers, list)
for server in enabled_servers:
    assert isinstance(server, str)

enabled_servers: list[str] = enabled_servers

# all servers
all_servers = {
    "searxng": StdioServerParameters(
        command="uvx",
        args=["mcp-searxng"],
        env={},
    ),
    "wolframalpha": StdioServerParameters(
        command="uvx",
        args=["mcp-wolfram-alpha"],
        env={
            "WOLFRAM_API_KEY": "abc",
        },
    ),
    
}

# servers to run
servers_to_run: dict[str, StdioServerParameters] = {}
for server in enabled_servers:
    servers_to_run[server] = all_servers[server]