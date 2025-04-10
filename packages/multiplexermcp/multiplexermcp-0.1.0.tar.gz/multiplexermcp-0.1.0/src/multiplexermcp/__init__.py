import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from pydantic import AnyUrl

from multiplexermcp.config import servers_to_run

from easymcp.client.ClientManager import ClientManager

# Create a server instance
server = Server("multiplexermcp") # type: ignore

# create client
client = ClientManager()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return await client.list_prompts()


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    return await client.read_prompt(name, arguments)


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return await client.list_resources()


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    resource = (await client.read_resource(uri)).contents
    if isinstance(resource, types.TextResourceContents):
        return resource.text
    elif isinstance(resource, types.BlobResourceContents):
        return resource.blob
    
    return "error"


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return await client.list_tools()


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    result = await client.call_tool(name, arguments)
    return result.content


async def run():
    await client.init(servers_to_run) # type: ignore

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    import asyncio
    asyncio.run(run())


if __name__ == "__main__":
    main()
