import asyncio
import os
import sys
import logging
from typing import Any
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify environment variables
API_TOKEN = os.getenv("YALA_EVENTS_API_TOKEN")
BASE_URL = os.getenv("BASE_URL")

if not API_TOKEN:
    logger.error("YALA_EVENTS_API_TOKEN environment variable not set")
    sys.exit(1)

server = Server("Yala Events Server")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def make_api_request(method: str, url: str, json: dict = None, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the yala.events API with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Making {method} request to {url}")
            response = await client.request(
                method=method,
                url=url,
                headers=HEADERS,
                json=json,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            return {"error": f"API error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources from yala.events."""
    data = await make_api_request("GET", f"{BASE_URL}/api/events")
    if not data or "data" not in data:
        return []
    
    return [
        types.Resource(
            uri=AnyUrl(f"event://yala/{event['id']}"),
            name=event['title'],
            description=f"Event on {event['startDateTime']}",
            mimeType="text/plain",  # Changed to text/plain to match python360
        )
        for event in data["data"]
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific event's details by its URI."""
    if uri.scheme != "event":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")
    
    event_id = uri.path.lstrip("/")
    data = await make_api_request("GET", f"{BASE_URL}/api/events/{event_id}")
    
    if not data or "data" not in data:
        raise ValueError(f"Event not found: {event_id}")
    
    event = data["data"]
    return f"Title: {event['title']}\nID: {event['id']}\nDate: {event['startDateTime']}\nContent: {event['content']}"

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="summarize-events",
            description="Creates a summary of all events",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Generate a prompt by combining arguments with event data."""
    if name != "summarize-events":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    data = await make_api_request("GET", f"{BASE_URL}/api/events")
    if not data or "data" not in data:
        event_summary = "No events available to summarize."
    else:
        event_summary = "\n".join(
            f"- {event['title']} (ID: {event['id']}): {event['startDateTime']}"
            if style == "brief" else
            f"- {event['title']} (ID: {event['id']}): {event['startDateTime']} - {event['content']}"
            for event in data["data"]
        )

    return types.GetPromptResult(
        description="Summarize the current events",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current events to summarize:{detail_prompt}\n\n{event_summary}",
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available tools for managing yala.events."""
    return [
        types.Tool(
            name="list-events",
            description="List events with optional date filter",
            inputSchema={
                "type": "object",
                "properties": {"date": {"type": "string"}}
            }
        ),
        types.Tool(
            name="create-event",
            description="Create a new event",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"},
                    "organization_id": {"type": "integer"}, "type_id": {"type": "integer"},
                    "category_id": {"type": "integer"}, "format_id": {"type": "integer"},
                    "covers": {"type": "array", "items": {"type": "string"}}, "is_private": {"type": "boolean"}
                },
                "required": ["title", "content", "date", "organization_id", "type_id", "category_id", "format_id", "covers", "is_private"]
            }
        ),
        types.Tool(
            name="get-event-details",
            description="Get details of a specific event",
            inputSchema={
                "type": "object",
                "properties": {"event_id": {"type": "integer"}},
                "required": ["event_id"]
            }
        ),
        types.Tool(name="get-organizations", description="List all organizations"),
        types.Tool(
            name="list-histories",
            description="List history records",
            inputSchema={
                "type": "object",
                "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}
            }
        ),
        # Add remaining tools similarly, ensuring inputSchema is either valid or omitted
        # For brevity, I'll include just a few more as examples
        types.Tool(
            name="list-modules",
            description="List modules with optional search",
            inputSchema={
                "type": "object",
                "properties": {"search": {"type": "string"}}
            }
        ),
        types.Tool(
            name="create-module",
            description="Create a new module",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"]
            }
        ),
        types.Tool(name="health-check", description="Perform a health check on the application"),
        # ... Add the other 25 tools here following the same pattern
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests for yala.events."""
    if name == "list-events":
        params = {"date": arguments.get("date")} if arguments and "date" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/events", params=params)
        if not data or "data" not in data:
            return [types.TextContent(type="text", text="No events found")]
        events = [f"Event: {e['title']} | Date: {e['startDateTime']} | ID: {e['id']}" for e in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(events))]

    elif name == "create-event":
        if not arguments:
            raise ValueError("Missing arguments")
        payload = {
            "title": arguments.get("title"), "content": arguments.get("content"), "startDateTime": arguments.get("date"),
            "organizationId": arguments.get("organization_id"), "typeId": arguments.get("type_id"),
            "categoryId": arguments.get("category_id"), "formatId": arguments.get("format_id"),
            "covers": arguments.get("covers"), "isPrivate": arguments.get("is_private")
        }
        data = await make_api_request("POST", f"{BASE_URL}/api/events", json=payload)
        if not data or "data" not in data:
            raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        event = data["data"]
        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Event created: {event['title']} (ID: {event['id']})")]

    elif name == "get-event-details":
        if not arguments or "event_id" not in arguments:
            raise ValueError("Missing event_id")
        data = await make_api_request("GET", f"{BASE_URL}/api/events/{arguments['event_id']}")
        if not data or "data" not in data:
            raise ValueError(f"Failed: {data.get('error', 'Event not found')}")
        event = data["data"]
        return [types.TextContent(type="text", text=f"Title: {event['title']}\nID: {event['id']}\nDate: {event['startDateTime']}\nContent: {event['content']}")]

    elif name == "get-organizations":
        data = await make_api_request("GET", f"{BASE_URL}/api/organizations")
        if not data or "data" not in data:
            return [types.TextContent(type="text", text="No organizations found")]
        orgs = [f"Organization: {org['name']} | ID: {org['id']}" for org in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(orgs))]

    elif name == "list-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/histories", params=params)
        if not data or "data" not in data:
            return [types.TextContent(type="text", text="No histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']} | Date: {h['createdAt']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-modules":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/modules", params=params)
        if not data or "data" not in data:
            return [types.TextContent(type="text", text="No modules found")]
        modules = [f"Module: {m['name']} | ID: {m['id']}" for m in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(modules))]

    elif name == "create-module":
        if not arguments or "name" not in arguments:
            raise ValueError("Missing name")
        data = await make_api_request("POST", f"{BASE_URL}/api/modules", json={"name": arguments["name"]})
        if not data or "data" not in data:
            raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        module = data["data"]
        return [types.TextContent(type="text", text=f"Module created: {module['name']} (ID: {module['id']})")]

    elif name == "health-check":
        data = await make_api_request("GET", f"{BASE_URL}/app/info/health-check")
        if not data:
            return [types.TextContent(type="text", text="Health check failed")]
        return [types.TextContent(type="text", text="Application is healthy")]

    # Add remaining tool handlers here following the same pattern
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Yala Events Server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())